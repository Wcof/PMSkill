"""Codex session discovery adapter."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from .constants import (
    CODEX_DEFAULT_HOME,
    CODEX_HOME_ENV,
    CODEX_INDEX_REL,
    CODEX_SESSIONS_REL,
)
from .discovery_shared import (
    Session,
    extract_text,
    is_subpath,
    iter_jsonl_files,
    read_jsonl,
)


_codex_home_cache: Optional[Path] = None


def _get_codex_home() -> Path:
    global _codex_home_cache
    if _codex_home_cache is None:
        env = os.environ.get(CODEX_HOME_ENV)
        _codex_home_cache = (
            Path(env).expanduser().resolve()
            if env
            else Path(CODEX_DEFAULT_HOME).expanduser().resolve()
        )
    return _codex_home_cache


def _codex_turns(entries: list[dict], since: str = "") -> list[tuple[str, str, str]]:
    turns: list[tuple[str, str, str]] = []
    cur_user: Optional[str] = None
    cur_ts: Optional[str] = None

    for entry in entries:
        if entry.get("type") != "response_item":
            continue
        payload = entry.get("payload", {})
        if not isinstance(payload, dict) or payload.get("type") != "message":
            continue
        role = payload.get("role", "")
        text = extract_text(payload.get("content", []), accepted_types=("input_text", "output_text"))
        ts = entry.get("timestamp", "")

        if role == "user" and text:
            cur_user = text
            cur_ts = ts
        elif role == "assistant" and text and cur_user:
            if since and cur_ts and cur_ts <= since:
                cur_user = cur_ts = None
                continue
            turns.append((cur_user, text, cur_ts or ts))
            cur_user = cur_ts = None

    return turns


def find_codex_home() -> Path:
    """Discover the Codex home directory."""
    return _get_codex_home()


def list_codex_sessions(
    project_cwd: str,
    since: str = "",
    codex_home: Optional[Path] = None,
    **_: object,
) -> list[Session]:
    home = codex_home or _get_codex_home()
    sessions_dir = home / CODEX_SESSIONS_REL
    if not sessions_dir.is_dir():
        return []

    # Build index lookup
    index_path = home / CODEX_INDEX_REL
    index_map: dict[str, dict] = {}
    if index_path.exists():
        for entry in read_jsonl(index_path):
            sid = entry.get("id", "")
            if sid:
                index_map[sid] = entry

    results: list[Session] = []
    for path, stem in iter_jsonl_files(sessions_dir, "rollout-*.jsonl", recursive=True):
        parts = stem.split("-", 6)
        sid = parts[6] if len(parts) >= 7 else stem

        entries = read_jsonl(path)
        header = next(
            (e.get("payload", {}) for e in entries if e.get("type") == "session_meta"),
            {},
        )
        if project_cwd and not is_subpath(header.get("cwd", ""), project_cwd):
            continue

        turns = _codex_turns(entries, since=since)
        info = index_map.get(sid, {})
        results.append(Session(
            id=sid,
            turns=turns,
            path=str(path),
            name=info.get("thread_name", ""),
        ))

    return results
