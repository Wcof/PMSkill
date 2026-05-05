"""
Bilingual metadata detection for passive collect sources.
"""

from __future__ import annotations

import re


FIELD_ALIASES = {
    "source": ("source", "来源"),
    "source_time": ("source_time", "recorded_at", "record_time", "记录时间"),
    "source_type": ("source_type", "材料类型"),
    "recorder": ("recorder", "recorded_by", "记录人"),
    "owner": ("owner", "responsible_person", "责任人"),
    "priority": ("priority", "优先级"),
}

# Core fields: must be present for "partial" status
CORE_FIELDS = ("source", "source_time")

# Fields required for "complete" status (source_type is recognized but not required)
COMPLETE_FIELDS = ("source", "source_time", "recorder", "owner", "priority")


def has_yaml_front_matter(content: str) -> bool:
    return content.startswith("---") and "\n---" in content[3:]


def has_metadata_field(content: str, aliases: tuple[str, ...]) -> bool:
    for alias in aliases:
        if re.search(rf"^\s*[-*]?\s*{re.escape(alias)}\s*[:：]\s*\S+", content, re.MULTILINE):
            return True
    return False


def _check_fields(content: str) -> tuple[bool, bool]:
    """Return (complete_present, core_present) for the given content."""
    core_present = all(
        has_metadata_field(content, FIELD_ALIASES[f]) for f in CORE_FIELDS
    )
    if not core_present:
        return False, False
    complete_present = all(
        has_metadata_field(content, FIELD_ALIASES[f]) for f in COMPLETE_FIELDS if f not in CORE_FIELDS
    )
    return complete_present, True


def metadata_status_for_text(content: str) -> str:
    """Return metadata completeness: complete / partial / missing.

    - complete: all recommended fields present
    - partial: core fields (source, source_time) present
    - missing: no recognizable metadata
    """
    # Check YAML front matter first
    if has_yaml_front_matter(content):
        body = content.split("---", 2)[1]
        all_ok, core_ok = _check_fields(body)
        if all_ok:
            return "complete"
        if core_ok:
            return "partial"

    # Check bullet-list metadata in full content
    all_ok, core_ok = _check_fields(content)
    if all_ok:
        return "complete"
    if core_ok:
        return "partial"
    return "missing"
