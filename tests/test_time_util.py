import os
from datetime import timezone, timedelta
from unittest.mock import patch

from scripts.lib.time_util import now_iso, now_id, _timezone_from_env


def test_now_iso_returns_iso_format():
    result = now_iso()
    # Should be like 2026-05-27T10:30:00+08:00
    assert "T" in result
    assert "+" in result or result.count("-") >= 3


def test_now_id_returns_yyyymmdd_hhmmss():
    result = now_id()
    assert len(result) == 15  # YYYYMMDD-HHMMSS
    assert result[8] == "-"
    assert result[:8].isdigit()
    assert result[9:].isdigit()


def test_timezone_from_env_default():
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("PRD_HELPER_UTC_OFFSET", None)
        tz = _timezone_from_env()
        assert tz == timezone(timedelta(hours=8))


def test_timezone_from_env_positive():
    with patch.dict(os.environ, {"PRD_HELPER_UTC_OFFSET": "+05:30"}):
        tz = _timezone_from_env()
        assert tz == timezone(timedelta(hours=5, minutes=30))


def test_timezone_from_env_negative():
    with patch.dict(os.environ, {"PRD_HELPER_UTC_OFFSET": "-05:00"}):
        tz = _timezone_from_env()
        assert tz == timezone(timedelta(hours=-5))


def test_timezone_from_env_utc():
    with patch.dict(os.environ, {"PRD_HELPER_UTC_OFFSET": "+00:00"}):
        tz = _timezone_from_env()
        assert tz == timezone.utc


def test_now_iso_contains_offset():
    result = now_iso()
    # Default offset is +08:00
    assert "+08:00" in result
