"""Source Anchor contract for Strong Trace and Weak Trace."""

from __future__ import annotations

from dataclasses import dataclass

from .markdown_util import has_field


TRACE_ANCHOR_FIELDS = ("source_id", "path", "locator")
QUOTE_FIELDS = ("quote", "paraphrase", "引用", "转述")


@dataclass(frozen=True)
class TraceQuality:
    strong: bool
    missing: list[str]


def has_source_anchor(block: str) -> bool:
    return trace_quality(block).strong


def trace_quality(block: str) -> TraceQuality:
    missing = [field for field in TRACE_ANCHOR_FIELDS if not has_field(block, field)]
    if not any(has_field(block, field) for field in QUOTE_FIELDS):
        missing.append("quote/paraphrase")
    return TraceQuality(strong=not missing, missing=missing)
