"""Shared utilities for AI coding tool session discovery."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator, Optional
from urllib.parse import unquote


class Session:
    """A discovered conversation session."""

    __slots__ = ("id", "name", "path", "turns")

    def __init__(
        self,
        id: str,
        turns: list[tuple[str, str, str]],
        path: str = "",
        name: str = "",
    ) -> None:
        self.id = id
        self.name = name
        self.path = path
        self.turns = turns


def read_jsonl(path: Path) -> list[dict]:
    """Parse a JSONL file and return all valid entries."""
    entries: list[dict] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def read_workspace_folder(ws_dir: Path) -> Optional[str]:
    """Read workspace.json and return the decoded folder path, or None."""
    ws_json = ws_dir / "workspace.json"
    if not ws_json.exists():
        return None
    try:
        with open(ws_json, encoding="utf-8") as f:
            data = json.load(f)
        folder = data.get("folder", "")
        if folder.startswith("file:///"):
            return unquote(folder[7:])
        return unquote(folder) if folder else None
    except (json.JSONDecodeError, OSError):
        return None


def extract_text(content: object, accepted_types: Optional[tuple[str, ...]] = None) -> str:
    """Extract text from message content.

    accepted_types: if set, only items whose "type" matches are included.
                    If None, any dict with a "text" key is included.
    Bare string items in lists are always included.
    """
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if isinstance(item, dict):
            if accepted_types is not None and item.get("type") not in accepted_types:
                continue
            t = item.get("text", "")
            if t:
                parts.append(str(t))
        elif isinstance(item, str):
            parts.append(item)
    return "\n".join(parts)


def is_subpath(child: str, parent: str) -> bool:
    """Check if child equals parent or is a descendant directory."""
    parent = parent.rstrip("/")
    return child == parent or child.startswith(parent + "/")


def iter_jsonl_files(directory: Path, pattern: str = "*.jsonl", recursive: bool = False) -> Iterator[tuple[Path, str]]:
    """Yield (path, stem) for JSONL files matching *pattern* in *directory*."""
    glob_fn = directory.rglob if recursive else directory.glob
    for p in sorted(glob_fn(pattern)):
        if p.is_file():
            yield p, p.stem
