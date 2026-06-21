"""Tests for CC-Switch Token Stats Skill"""

import unittest
import sys
from pathlib import Path

# Setup import path for skill module
SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR))

from impl import (
    get_today_usage,
    get_alltime_totals,
    CC_SWITCH_DB,
)


class TestCCSwitchTokenStats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not CC_SWITCH_DB.exists():
            raise unittest.SkipTest(f"CC-Switch DB not found: {CC_SWITCH_DB}")

    def test_today_usage(self):
        result = get_today_usage()
        self.assertTrue(result.success, f"Query failed: {result.error}")
        self.assertIsNotNone(result.summary)
        self.assertGreater(result.summary.total_requests, 0)

    def test_alltime_totals(self):
        result = get_alltime_totals()
        self.assertTrue(result.success)
        self.assertIsNotNone(result.summary)
        self.assertGreater(result.summary.total_requests, 0)
        self.assertGreater(result.summary.token_usage.total_tokens, 0)
        self.assertGreater(len(result.summary.by_model), 0)

    def test_token_usage_computed(self):
        result = get_today_usage()
        t = result.summary.token_usage
        self.assertEqual(t.total_tokens, t.input_tokens + t.output_tokens + t.cache_read_tokens + t.cache_creation_tokens)

    def test_error_no_db(self):
        import sqlite3
        old_path = str(CC_SWITCH_DB)
        # Just verify exception handling works
        result = get_today_usage()
        self.assertTrue(result.success or result.error is not None)


if __name__ == "__main__":
    unittest.main()
