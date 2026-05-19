"""
时间工具：统一时间戳生成。
"""

import os
from datetime import datetime, timezone, timedelta


def _timezone_from_env() -> timezone:
    raw = os.getenv("PRD_HELPER_UTC_OFFSET", "+08:00")
    sign = -1 if raw.startswith("-") else 1
    value = raw[1:] if raw[:1] in "+-" else raw
    hours, _, minutes = value.partition(":")
    return timezone(sign * timedelta(hours=int(hours or "0"), minutes=int(minutes or "0")))


TZ = _timezone_from_env()


def now_iso() -> str:
    """返回东八区当前时间的 ISO 格式字符串。"""
    return datetime.now(TZ).isoformat(timespec="seconds")


def now_id() -> str:
    """返回东八区当前时间的 ID 格式字符串（YYYYMMDD-HHMMSS）。"""
    return datetime.now(TZ).strftime("%Y%m%d-%H%M%S")
