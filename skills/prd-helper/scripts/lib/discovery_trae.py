"""Trae / Trae CN session discovery adapter."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Optional

from .discovery_shared import (
    Session,
    extract_text,
    is_subpath,
    read_workspace_folder,
)


_TRAE_HOMES: Optional[tuple[Path, ...]] = None
_TRAE_WS_REL = "User/workspaceStorage"
_TRAE_STORAGE_KEY = "memento/icube-ai-agent-storage"


def _trae_sessions(ws_db: Path) -> list[dict]:
    if not ws_db.exists():
        return []
    try:
        conn = sqlite3.connect(str(ws_db))
        cur = conn.cursor()
        cur.execute("SELECT value FROM ItemTable WHERE key = ?", (_TRAE_STORAGE_KEY,))
        row = cur.fetchone()
        conn.close()
        if not row:
            return []
        return json.loads(row[0]).get("list", [])
    except (sqlite3.Error, json.JSONDecodeError, OSError):
        return []


def _trae_turns(messages: list[dict]) -> list[tuple[str, str, str]]:
    turns: list[tuple[str, str, str]] = []
    cur_user: Optional[str] = None
    for msg in messages:
        text = extract_text(msg.get("content", ""))
        role = msg.get("role", "")
        if role == "user" and text:
            cur_user = text
        elif role == "assistant" and text and cur_user:
            turns.append((cur_user, text, ""))
            cur_user = None
    return turns


def _get_trae_homes() -> tuple[Path, ...]:
    global _TRAE_HOMES
    if _TRAE_HOMES is None:
        _TRAE_HOMES = tuple(
            Path(p).expanduser().resolve()
            for p in (
                "~/Library/Application Support/Trae",
                "~/Library/Application Support/Trae CN",
            )
            if Path(p).expanduser().is_dir()
        )
    return _TRAE_HOMES


def list_trae_sessions(project_cwd: str, **_: object) -> list[Session]:
    results: list[Session] = []
    for home in _get_trae_homes():
        ws_base = home / _TRAE_WS_REL
        if not ws_base.is_dir():
            continue
        project_cwd_norm = project_cwd.rstrip("/")
        for ws_dir in sorted(ws_base.iterdir()):
            if not ws_dir.is_dir():
                continue
            folder = read_workspace_folder(ws_dir)
            if not folder or not is_subpath(folder.rstrip("/"), project_cwd_norm):
                continue
            for session in _trae_sessions(ws_dir / "state.vscdb"):
                sid = session.get("sessionId", "")
                turns = _trae_turns(session.get("messages", []))
                if turns:
                    results.append(Session(id=sid, turns=turns, path=str(ws_dir)))
    return results
