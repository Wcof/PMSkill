"""Codex session discovery and parsing utilities.

Discovers the Codex home directory, locates session files, and parses
JSONL session data to extract user/assistant conversation turns.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from .constants import CODEX_DEFAULT_HOME, CODEX_HOME_ENV, CODEX_INDEX_REL, CODEX_SESSIONS_REL


def find_codex_home() -> Path:
    """Discover the Codex home directory.

    Priority: CODEX_HOME env var > ~/.codex default.
    """
    env = os.environ.get(CODEX_HOME_ENV)
    if env:
        return Path(env).expanduser().resolve()
    return Path(CODEX_DEFAULT_HOME).expanduser().resolve()


def find_session_index(home: Path) -> Optional[Path]:
    """Locate session_index.jsonl in Codex home."""
    index = home / CODEX_INDEX_REL
    return index if index.exists() else None


def find_sessions_dir(home: Path) -> Optional[Path]:
    """Locate the sessions directory in Codex home."""
    sessions = home / CODEX_SESSIONS_REL
    return sessions if sessions.is_dir() else None


def parse_session_index(home: Path) -> list[dict]:
    """Parse session_index.jsonl and return list of session metadata."""
    index_path = find_session_index(home)
    if not index_path:
        return []
    entries = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def parse_session_jsonl(path: Path) -> list[dict]:
    """Parse a Codex session JSONL file and return all entries."""
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def filter_turns(
    entries: list[dict],
    since: str = "",
    project_cwd: str = "",
) -> list[tuple[str, str, str]]:
    """Extract (user_query, agent_answer, timestamp) triples from session entries.

    Only returns complete pairs where both user query and agent answer are present.
    Filters by timestamp if ``since`` is provided (ISO 8601 comparison).

    Returns:
        List of (user_query, agent_answer, timestamp) tuples.
    """
    turns: list[tuple[str, str, str]] = []
    current_user: Optional[str] = None
    current_ts: Optional[str] = None
    session_cwd: Optional[str] = None

    for entry in entries:
        etype = entry.get("type", "")
        payload = entry.get("payload", {})

        # Extract session metadata for cwd filtering
        if etype == "session_meta" and isinstance(payload, dict):
            session_cwd = payload.get("cwd", "")

        # Filter by project cwd if specified
        if project_cwd and session_cwd and project_cwd != session_cwd:
            continue

        if etype != "response_item":
            continue
        if not isinstance(payload, dict):
            continue
        if payload.get("type") != "message":
            continue

        role = payload.get("role", "")
        content = payload.get("content", [])
        text = _extract_text(content)
        ts = entry.get("timestamp", "")

        if role == "user" and text:
            current_user = text
            current_ts = ts
        elif role == "assistant" and text and current_user:
            # Check since filter
            if since and current_ts and current_ts <= since:
                current_user = None
                current_ts = None
                continue
            turns.append((current_user, text, current_ts or ts))
            current_user = None
            current_ts = None

    return turns


def _extract_text(content: list) -> str:
    """Extract text from a content array."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = []
    for item in content:
        if isinstance(item, dict) and item.get("type") in ("input_text", "output_text"):
            parts.append(item.get("text", ""))
        elif isinstance(item, str):
            parts.append(item)
    return "\n".join(parts)


def list_project_sessions(
    home: Path,
    project_cwd: str,
    since: str = "",
) -> list[dict]:
    """List Codex sessions for a specific project.

    Scans session_index.jsonl and finds JSONL files whose session_meta.cwd matches.
    Returns list of dicts with keys: id, thread_name, updated_at, path, turns.
    """
    sessions_dir = find_sessions_dir(home)
    if not sessions_dir:
        return []

    index_entries = parse_session_index(home)
    if not index_entries:
        return []

    # Collect all session IDs from index
    session_ids: dict[str, dict] = {}
    for entry in index_entries:
        sid = entry.get("id", "")
        if sid:
            session_ids[sid] = entry

    # Find JSONL files and match with sessions
    results = []
    for jsonl_path in sessions_dir.rglob("rollout-*.jsonl"):
        # Extract session ID from filename: rollout-{time}-{uuid}.jsonl
        stem = jsonl_path.stem
        parts = stem.split("-", 6)
        if len(parts) < 7:
            continue
        sid = parts[6]

        # Parse and filter by project cwd
        entries = parse_session_jsonl(jsonl_path)
        meta_cwd = ""
        for entry in entries:
            if entry.get("type") == "session_meta":
                meta_cwd = entry.get("payload", {}).get("cwd", "")
                break

        if project_cwd and meta_cwd != project_cwd:
            continue

        # Extract turns
        turns = filter_turns(entries, since=since)

        index_info = session_ids.get(sid, {})
        results.append({
            "id": sid,
            "thread_name": index_info.get("thread_name", ""),
            "updated_at": index_info.get("updated_at", ""),
            "path": str(jsonl_path),
            "turns": turns,
            "cwd": meta_cwd,
        })

    return results
