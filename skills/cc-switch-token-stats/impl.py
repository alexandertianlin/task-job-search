"""CC-Switch Token Stats Skill - Implementation"""

import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

from schema import (
    TokenUsage,
    ModelUsage,
    HourlyUsage,
    DailyUsage,
    UsageSummary,
    StatusSummary,
    UsageQueryResult,
)

CC_SWITCH_DB = Path.home() / ".cc-switch" / "cc-switch.db"


def _get_connection():
    if not CC_SWITCH_DB.exists():
        raise FileNotFoundError(f"CC-Switch DB not found: {CC_SWITCH_DB}")
    conn = sqlite3.connect(str(CC_SWITCH_DB))
    conn.row_factory = sqlite3.Row
    return conn


def _get_today_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def get_today_usage():
    t0 = time.time()
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        today = _get_today_str()

        cursor.execute("""
            SELECT
                COUNT(*) as reqs,
                COALESCE(SUM(input_tokens), 0) as inp,
                COALESCE(SUM(output_tokens), 0) as out,
                COALESCE(SUM(cache_read_tokens), 0) as cache_r,
                COALESCE(SUM(cache_creation_tokens), 0) as cache_c,
                COALESCE(SUM(CAST(total_cost_usd AS REAL)), 0) as cost
            FROM proxy_request_logs
            WHERE date(created_at, "unixepoch") = ?
        """, [today])
        total = dict(cursor.fetchone())

        cursor.execute("""
            SELECT
                model,
                COUNT(*) as reqs,
                COALESCE(SUM(input_tokens), 0) as inp,
                COALESCE(SUM(output_tokens), 0) as out,
                COALESCE(SUM(cache_read_tokens), 0) as cache_r,
                COALESCE(SUM(cache_creation_tokens), 0) as cache_c,
                COALESCE(SUM(CAST(total_cost_usd AS REAL)), 0) as cost
            FROM proxy_request_logs
            WHERE date(created_at, "unixepoch") = ?
            GROUP BY model
            ORDER BY inp DESC
        """, [today])
        by_model = []
        for r in cursor.fetchall():
            d = dict(r)
            by_model.append(ModelUsage(
                model=d["model"],
                request_count=d["reqs"],
                token_usage=TokenUsage(
                    input_tokens=d["inp"],
                    output_tokens=d["out"],
                    cache_read_tokens=d["cache_r"],
                    cache_creation_tokens=d["cache_c"],
                ),
                total_cost_usd=d["cost"],
            ))

        cursor.execute("""
            SELECT
                app_type,
                COUNT(*) as reqs,
                COALESCE(SUM(input_tokens), 0) as inp,
                COALESCE(SUM(output_tokens), 0) as out,
                COALESCE(SUM(cache_read_tokens), 0) as cache_r,
                COALESCE(SUM(cache_creation_tokens), 0) as cache_c,
                COALESCE(SUM(CAST(total_cost_usd AS REAL)), 0) as cost
            FROM proxy_request_logs
            WHERE date(created_at, "unixepoch") = ?
            GROUP BY app_type
            ORDER BY inp DESC
        """, [today])
        by_app = []
        for r in cursor.fetchall():
            d = dict(r)
            by_app.append(ModelUsage(
                model=d["app_type"],
                request_count=d["reqs"],
                token_usage=TokenUsage(
                    input_tokens=d["inp"],
                    output_tokens=d["out"],
                    cache_read_tokens=d["cache_r"],
                    cache_creation_tokens=d["cache_c"],
                ),
                total_cost_usd=d["cost"],
            ))

        conn.close()
        tu = TokenUsage(
            input_tokens=total["inp"],
            output_tokens=total["out"],
            cache_read_tokens=total["cache_r"],
            cache_creation_tokens=total["cache_c"],
        )
        lat = (time.time() - t0) * 1000
        return UsageQueryResult(
            success=True,
            summary=UsageSummary(
                total_requests=total["reqs"],
                token_usage=tu,
                total_cost_usd=total["cost"],
                by_model=by_model,
                by_app_type=by_app,
                time_range=today,
            ),
            latency_ms=lat,
        )
    except Exception as e:
        return UsageQueryResult(success=False, error=str(e))

def get_alltime_totals():
    t0 = time.time()
    try:
        conn = _get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) as reqs,
                COALESCE(SUM(input_tokens), 0) as inp,
                COALESCE(SUM(output_tokens), 0) as out,
                COALESCE(SUM(cache_read_tokens), 0) as cache_r,
                COALESCE(SUM(cache_creation_tokens), 0) as cache_c,
                COALESCE(SUM(CAST(total_cost_usd AS REAL)), 0) as cost,
                COALESCE(MIN(created_at), 0) as first_ts,
                COALESCE(MAX(created_at), 0) as last_ts
            FROM proxy_request_logs
        """)
        total = dict(cursor.fetchone())

        first_ts = total["first_ts"]
        last_ts = total["last_ts"]
        time_range = ""
        if first_ts and last_ts:
            start = datetime.fromtimestamp(first_ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
            end = datetime.fromtimestamp(last_ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
            time_range = f"{start} ~ {end}"

        cursor.execute("""
            SELECT
                model,
                COUNT(*) as reqs,
                COALESCE(SUM(input_tokens), 0) as inp,
                COALESCE(SUM(output_tokens), 0) as out,
                COALESCE(SUM(cache_read_tokens), 0) as cache_r,
                COALESCE(SUM(cache_creation_tokens), 0) as cache_c,
                COALESCE(SUM(CAST(total_cost_usd AS REAL)), 0) as cost
            FROM proxy_request_logs
            GROUP BY model
            ORDER BY inp DESC
        """)
        by_model = []
        for r in cursor.fetchall():
            d = dict(r)
            by_model.append(ModelUsage(
                model=d["model"],
                request_count=d["reqs"],
                token_usage=TokenUsage(
                    input_tokens=d["inp"],
                    output_tokens=d["out"],
                    cache_read_tokens=d["cache_r"],
                    cache_creation_tokens=d["cache_c"],
                ),
                total_cost_usd=d["cost"],
            ))

        conn.close()
        tu = TokenUsage(
            input_tokens=total["inp"],
            output_tokens=total["out"],
            cache_read_tokens=total["cache_r"],
            cache_creation_tokens=total["cache_c"],
        )
        lat = (time.time() - t0) * 1000
        return UsageQueryResult(
            success=True,
            summary=UsageSummary(
                total_requests=total["reqs"],
                token_usage=tu,
                total_cost_usd=total["cost"],
                by_model=by_model,
                time_range=time_range,
            ),
            latency_ms=lat,
        )
    except Exception as e:
        return UsageQueryResult(success=False, error=str(e))


def print_summary(result):
    if not result.success:
        print("Query failed: " + result.error)
        return
    s = result.summary
    if s:
        t = s.token_usage
        print("== Time range: " + s.time_range + " ==")
        print("Requests:   " + str(s.total_requests))
        print("Input:      " + str(t.input_tokens))
        print("Output:     " + str(t.output_tokens))
        print("Cache R:    " + str(t.cache_read_tokens))
        print("Cache C:    " + str(t.cache_creation_tokens))
        print("Total:      " + str(t.total_tokens))
        print("Cost:       $" + format(s.total_cost_usd, ".4f"))
        print()
        if s.by_model:
            print("By model:")
            for m in s.by_model:
                mt = m.token_usage
                print("  " + m.model.ljust(30) + ": reqs=" + str(m.request_count) + "  in=" + str(mt.input_tokens) + "  out=" + str(mt.output_tokens) + "  cache=" + str(mt.cache_read_tokens) + "  " + format(m.total_cost_usd, ".4f"))

    print("Latency: " + format(result.latency_ms, ".1f") + "ms")
