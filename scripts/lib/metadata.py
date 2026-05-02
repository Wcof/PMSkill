"""
Bilingual metadata detection for passive collect sources.
"""

from __future__ import annotations

import re


FIELD_ALIASES = {
    "source": ("source", "来源"),
    "source_time": ("source_time", "recorded_at", "record_time", "记录时间"),
    "recorder": ("recorder", "recorded_by", "记录人"),
    "owner": ("owner", "responsible_person", "责任人"),
    "priority": ("priority", "优先级"),
}


def has_yaml_front_matter(content: str) -> bool:
    return content.startswith("---") and "\n---" in content[3:]


def has_metadata_field(content: str, aliases: tuple[str, ...]) -> bool:
    for alias in aliases:
        if re.search(rf"^\s*[-*]?\s*{re.escape(alias)}\s*[:：]\s*\S+", content, re.MULTILINE):
            return True
    return False


def metadata_status_for_text(content: str) -> str:
    """Return complete when required bilingual metadata fields are present."""
    if has_yaml_front_matter(content):
        body = content.split("---", 2)[1]
        if all(has_metadata_field(body, aliases) for aliases in FIELD_ALIASES.values()):
            return "complete"
    if all(has_metadata_field(content, aliases) for aliases in FIELD_ALIASES.values()):
        return "complete"
    return "missing"
