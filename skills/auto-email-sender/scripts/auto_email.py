#!/usr/bin/env python3
"""
田霖 - 自动发送邮件投递系统
用 Gmail 批量发送简历 + 自然语言求职信

特色:
- 密码优先从环境变量 GMAIL_APP_PASSWORD 读取（安全），再读 config 文件
- 自动尝试 SMTP_SSL (465) → STARTTLS (587) 双端口
- 支持 Gmail API OAuth 2.0
- 逐目标自定义简历附件
- 投递状态追踪

用法:
  python src/auto_email.py setup         配置发件人信息
  python src/auto_email.py list          查看待投递目标
  python src/auto_email.py send          发送所有待投递邮件
  python src/auto_email.py send <id>     发送指定目标
  python src/auto_email.py status        查看投递状态
  python src/auto_email.py dry-run       试运行（不真实发送）
"""

import argparse
import json
import os
import re
import smtplib
import ssl
import sys
import datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path

import certifi

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
APPS_DIR = BASE_DIR / "applications"
OUTPUTS_DIR = BASE_DIR / "outputs"

CONFIG_FILE = CONFIG_DIR / "email_targets.json"


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------
def load_config():
    if not CONFIG_FILE.exists():
        print(f"[错误] 配置文件不存在: {CONFIG_FILE}")
        print("请先运行 python src/auto_email.py setup")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f"[OK] 配置已保存: {CONFIG_FILE}")


def load_send_log():
    cfg = load_config()
    log_path = BASE_DIR / cfg.get("email_log", "outputs/email_send_log.json")
    if log_path.exists():
        with open(log_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_send_log(log):
    cfg = load_config()
    log_path = BASE_DIR / cfg.get("email_log", "outputs/email_send_log.json")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Password: env var first, config file as fallback
# ---------------------------------------------------------------------------
def get_app_password(cfg):
    """Read password from env var GMAIL_APP_PASSWORD, fallback to config file."""
    env_pwd = os.environ.get("GMAIL_APP_PASSWORD")
    if env_pwd:
        return env_pwd
    return cfg["sender"].get("app_password")


# ---------------------------------------------------------------------------
# Markdown → HTML (lightweight)
# ---------------------------------------------------------------------------
def md_to_html(text):
    """Simple markdown to HTML conversion for cover letters."""
    lines = text.split("\n")
    html_parts = []
    in_list = False

    for line in lines:
        stripped = line.strip()

        # Headers
        if stripped.startswith("### "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h3>{stripped[4:]}</h3>")
        elif stripped.startswith("## "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("# "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<h1>{stripped[2:]}</h1>")
        elif stripped == "---":
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append("<hr>")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{stripped[2:]}</li>")
        elif stripped == "":
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append("<br>")
        elif "**" in stripped:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            processed = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
            html_parts.append(f"<p>{processed}</p>")
        else:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f"<p>{stripped}</p>")

    if in_list:
        html_parts.append("</ul>")

    return "\n".join(html_parts)


def build_email_body(target, cfg):
    """Build HTML email body from cover letter markdown."""
    cover_path = BASE_DIR / target["cover_letter"]
    if not cover_path.exists():
        print(f"[警告] 求职信文件不存在: {cover_path}")
        return "<p>求职信待补充</p>"

    md_text = cover_path.read_text(encoding="utf-8")
    html_body = md_to_html(md_text)

    html_template = f"""\
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; line-height: 1.6; color: #333; max-width: 680px; margin: 0 auto; padding: 20px;">
<div style="background: #f8f9fa; border-radius: 8px; padding: 24px;">
{html_body}
</div>
<hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
<p style="font-size: 12px; color: #999;">
  Sent via 田霖自动投递系统 | {datetime.date.today().isoformat()}
</p>
</body>
</html>"""
    return html_template


# ---------------------------------------------------------------------------
# Gmail SMTP sender (supports 465 SSL + 587 STARTTLS)
# ---------------------------------------------------------------------------
def send_via_smtp(sender_email, app_password, to_addr, subject, html_body, attachment_path=None):
    """Send email via Gmail SMTP. Auto-tries SSL(465) then STARTTLS(587)."""
    msg = MIMEMultipart("mixed")
    msg["From"] = sender_email
    msg["To"] = to_addr
    msg["Subject"] = subject

    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(alt_part)

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename(attachment_path)
        part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
        msg.attach(part)

    ctx = ssl.create_default_context(cafile=certifi.where())

    # Try port 465 (SSL) first, fallback to 587 (STARTTLS)
    last_err = None
    for port, use_ssl in [(465, True), (587, False)]:
        try:
            if use_ssl:
                with smtplib.SMTP_SSL("smtp.gmail.com", port, context=ctx, timeout=30) as server:
                    server.login(sender_email, app_password)
                    server.sendmail(sender_email, to_addr, msg.as_string())
            else:
                with smtplib.SMTP("smtp.gmail.com", port, timeout=30) as server:
                    server.starttls(context=ctx)
                    server.login(sender_email, app_password)
                    server.sendmail(sender_email, to_addr, msg.as_string())
            return  # Success
        except Exception as e:
            last_err = e
            continue

    raise last_err  # Both ports failed


# ---------------------------------------------------------------------------
# Gmail API sender
# ---------------------------------------------------------------------------
def send_via_api(sender_email, credentials_path, to_addr, subject, html_body, attachment_path=None):
    """Send email via Gmail API with OAuth 2.0."""
    try:
        import google.auth
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        import base64
    except ImportError:
        print("[错误] Gmail API 需要额外安装依赖:")
        print("  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
        sys.exit(1)

    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

    creds = None
    token_path = os.path.join(os.path.dirname(credentials_path), "gmail_token.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())

    msg = MIMEMultipart("mixed")
    msg["From"] = sender_email
    msg["To"] = to_addr
    msg["Subject"] = subject

    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(alt_part)

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename(attachment_path)
        part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
        msg.attach(part)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service = build("gmail", "v1", credentials=creds)
    service.users().messages().send(userId="me", body={"raw": raw}).execute()


# ---------------------------------------------------------------------------
# CLI Commands
# ---------------------------------------------------------------------------
def cmd_setup(args):
    """交互式配置发件人信息"""
    cfg = load_config() if CONFIG_FILE.exists() else {
        "sender": {
            "email": "alexandertianlin@gmail.com",
            "name": "田霖",
            "method": "smtp",
            "app_password": None,
            "credentials_path": None,
        },
        "resume_pdf": "outputs/Lin_Tian_Resume_EN.pdf",
        "email_log": "outputs/email_send_log.json",
        "targets": [],
    }

    print("=" * 50)
    print("    田霖 - 自动邮件投递系统 配置")
    print("=" * 50)
    print()
    print("[提示] 也可通过环境变量设置密码（更安全）:")
    print("  export GMAIL_APP_PASSWORD=your16charcode")
    print()

    default = cfg["sender"].get("email", "alexandertianlin@gmail.com")
    val = input(f"发件人 Gmail [{default}]: ").strip()
    if val:
        cfg["sender"]["email"] = val

    default = cfg["sender"].get("name", "田霖")
    val = input(f"发件人姓名 [{default}]: ").strip()
    if val:
        cfg["sender"]["name"] = val

    print("\n选择发送方式:")
    print("  1) SMTP + App Password (推荐，无需额外依赖)")
    print("  2) Gmail API + OAuth 2.0 (需要 Google Cloud 项目)")
    choice = input("请选择 [1]: ").strip() or "1"

    if choice == "1":
        cfg["sender"]["method"] = "smtp"
        cfg["sender"]["credentials_path"] = None
        pwd = input("Gmail App Password (留空则用环境变量 GMAIL_APP_PASSWORD): ").strip()
        if pwd:
            cfg["sender"]["app_password"] = pwd
        print("\n[提示] App Password 获取方式:")
        print("  1. 开启 Gmail 两步验证: https://myaccount.google.com/security")
        print("  2. 生成 App Password: https://myaccount.google.com/apppasswords")
        print("  3. 选择 'Mail' + 'Mac'，复制生成的16位密码")
    else:
        cfg["sender"]["method"] = "api"
        cfg["sender"]["app_password"] = None
        creds = input("OAuth 2.0 客户端 JSON 路径 (credentials.json): ").strip()
        if creds:
            cfg["sender"]["credentials_path"] = creds

    default = cfg.get("resume_pdf") or ""
    val = input(f"\n简历 PDF 路径 [{default}]: ").strip()
    if val:
        cfg["resume_pdf"] = val
    elif default:
        cfg["resume_pdf"] = default

    save_config(cfg)
    print("\n✅ 配置完成！运行以下命令:")
    print("  python src/auto_email.py list      查看投递目标")
    print("  python src/auto_email.py send      发送邮件")
    print("  python src/auto_email.py dry-run   试运行")
    print()
    print("  或用环境变量设置密码（不写进文件）:")
    print("  export GMAIL_APP_PASSWORD=your16charcode")
    print("  python src/auto_email.py send")


def cmd_list(args):
    """列出所有投递目标"""
    cfg = load_config()
    log = load_send_log()

    has_env_pwd = bool(os.environ.get("GMAIL_APP_PASSWORD"))
    has_cfg_pwd = bool(cfg["sender"].get("app_password"))
    has_api_creds = bool(cfg["sender"].get("credentials_path"))
    sender_ok = has_env_pwd or has_cfg_pwd or has_api_creds

    resume_ok = cfg.get("resume_pdf") and os.path.exists(BASE_DIR / cfg["resume_pdf"]) if cfg.get("resume_pdf") else False

    print("=" * 60)
    print(f"  发件人: {cfg['sender']['email']}")
    print(f"  方式: {'SMTP (465/587)' if cfg['sender']['method'] == 'smtp' else 'Gmail API OAuth 2.0'}")
    print(f"  密码来源: {'环境变量' if has_env_pwd else '配置文件' if has_cfg_pwd else '未设置'}")
    print(f"  配置状态: {'✅ 已配置' if sender_ok else '❌ 未配置'}")
    print(f"  简历: {'✅ 已就绪' if resume_ok else '⚠️ 未指定'}")
    print("=" * 60)

    enabled = [t for t in cfg["targets"] if t.get("enabled", True)]
    print(f"\n待投递目标 ({len(enabled)} 个):")
    print("-" * 60)

    for t in enabled:
        tid = t["id"]
        sent_info = log.get(tid, {})
        status = "✅ 已发送" if sent_info.get("sent") else "⏳ 待投递"
        sent_at = f" ({sent_info['sent_at']})" if sent_info.get("sent_at") else ""
        print(f"  [{t['priority']}] {t['company']} - {t['position']}")
        print(f"       收件人: {t['to']}")
        print(f"       求职信: {t['cover_letter']}")
        print(f"       状态: {status}{sent_at}")
        if sent_info.get("error"):
            print(f"       上次错误: {sent_info['error']}")
        print()


def cmd_dry_run(args):
    """试运行——预览邮件内容但不发送"""
    cfg = load_config()
    if args.target_id:
        target = next((t for t in cfg["targets"] if t["id"] == args.target_id), None)
        if not target:
            print(f"[错误] 未找到目标: {args.target_id}")
            sys.exit(1)
        targets = [target]
    else:
        targets = [t for t in cfg["targets"] if t.get("enabled", True)]

    print(f"DRY RUN - 预览 {len(targets)} 封邮件\n")

    for t in targets:
        print("=" * 60)
        print(f"  收件人:  {t['to']}")
        print(f"  主题:    {t['subject']}")
        print(f"  求职信:  {t['cover_letter']}")

        cover_path = BASE_DIR / t["cover_letter"]
        if cover_path.exists():
            print(f"\n  --- 求职信预览 ({cover_path.name}) ---")
            content = cover_path.read_text(encoding="utf-8")
            print(content[:500])
            if len(content) > 500:
                print("  ... (truncated)")

        target_resume = t.get("resume_pdf") or cfg.get("resume_pdf")
        if target_resume:
            rp = BASE_DIR / target_resume
            print(f"\n  附件: {rp.name} ({'✅ 文件存在' if rp.exists() else '❌ 文件不存在'})")
        print()


def cmd_send(args):
    """发送邮件"""
    cfg = load_config()
    sender = cfg["sender"]

    password = get_app_password(cfg)
    if not password and not sender.get("credentials_path"):
        print("[错误] App Password 未设置。两种方式:")
        print("  1. export GMAIL_APP_PASSWORD=your16charcode")
        print("  2. python src/auto_email.py setup (写入配置文件)")
        sys.exit(1)

    # Which targets?
    if args.target_id:
        target = next((t for t in cfg["targets"] if t["id"] == args.target_id), None)
        if not target:
            print(f"[错误] 未找到目标: {args.target_id}")
            sys.exit(1)
        targets = [target]
    else:
        targets = [t for t in cfg["targets"] if t.get("enabled", True)]

    log = load_send_log()
    success_count = 0
    fail_count = 0

    print(f"\n开始发送 {len(targets)} 封邮件...\n")

    for t in targets:
        tid = t["id"]
        print(f"[{t['company']}] 正在发送 -> {t['to']} ...", end=" ", flush=True)

        try:
            html_body = build_email_body(t, cfg)

            # Per-target resume path
            target_resume = t.get("resume_pdf") or cfg.get("resume_pdf")
            resume_path = None
            if target_resume:
                rp = BASE_DIR / target_resume
                if rp.exists():
                    resume_path = str(rp)
                else:
                    print(f"\n[警告] 简历文件不存在: {rp}")

            if sender["method"] == "api":
                send_via_api(
                    sender_email=sender["email"],
                    credentials_path=sender["credentials_path"],
                    to_addr=t["to"],
                    subject=t["subject"],
                    html_body=html_body,
                    attachment_path=resume_path,
                )
            else:
                send_via_smtp(
                    sender_email=sender["email"],
                    app_password=password,
                    to_addr=t["to"],
                    subject=t["subject"],
                    html_body=html_body,
                    attachment_path=resume_path,
                )

            print("✅")
            log[tid] = {
                "sent": True,
                "sent_at": datetime.datetime.now().isoformat(),
                "error": None,
            }
            success_count += 1

        except Exception as e:
            print(f"❌ {e}")
            log[tid] = {
                "sent": False,
                "sent_at": None,
                "error": str(e),
            }
            fail_count += 1

    save_send_log(log)

    print(f"\n{'=' * 40}")
    print(f"  发送完成: ✅ {success_count} 成功, ❌ {fail_count} 失败")
    print(f"  共 {len(targets)} 封")
    if os.environ.get("GMAIL_APP_PASSWORD"):
        print("  (密码来源: 环境变量 GMAIL_APP_PASSWORD)")


def cmd_status(args):
    """查看投递状态"""
    cfg = load_config()
    log = load_send_log()

    has_env_pwd = bool(os.environ.get("GMAIL_APP_PASSWORD"))

    total = len(cfg["targets"])
    sent = sum(1 for t in cfg["targets"] if log.get(t["id"], {}).get("sent"))
    failed = sum(1 for t in cfg["targets"] if log.get(t["id"], {}).get("error"))
    pending = total - sent - failed

    print("=" * 50)
    print("  投递状态总览")
    print("=" * 50)
    print(f"  全部目标: {total}")
    print(f"  ✅ 已发送: {sent}")
    print(f"  ❌ 失败:   {failed}")
    print(f"  ⏳ 待发:   {max(0, pending)}")
    print()
    if has_env_pwd:
        print("  🔐 密码: 环境变量 GMAIL_APP_PASSWORD")
    print()

    for t in cfg["targets"]:
        info = log.get(t["id"], {})
        if info.get("sent"):
            status = f"✅ {info['sent_at'][:19]}"
        elif info.get("error"):
            status = f"❌ {info['error'][:60]}"
        else:
            status = "⏳ 待投递"
        print(f"  [{t['company']:25s}] {status}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="田霖 - 自动发送邮件投递系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("setup", help="交互式配置发件人信息")
    sub.add_parser("list", help="列出所有投递目标及状态")

    dry = sub.add_parser("dry-run", help="预览邮件内容（不真实发送）")
    dry.add_argument("target_id", nargs="?", help="指定目标 ID（可选）")

    send = sub.add_parser("send", help="发送邮件")
    send.add_argument("target_id", nargs="?", help="指定目标 ID（可选，默认全部）")

    sub.add_parser("status", help="查看投递状态")

    args = parser.parse_args()

    if args.command == "setup":
        cmd_setup(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "dry-run":
        cmd_dry_run(args)
    elif args.command == "send":
        cmd_send(args)
    elif args.command == "status":
        cmd_status(args)


if __name__ == "__main__":
    main()
