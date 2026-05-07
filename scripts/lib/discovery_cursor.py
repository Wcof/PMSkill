"""Cursor session discovery adapter."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Optional

from .discovery_shared import (
    Session,
    is_subpath,
    read_workspace_folder,
)


_cursor_home = Path("~/Library/Application Support/Cursor").expanduser()
_cursor_ws_base = _cursor_home / "User" / "workspaceStorage"
_cursor_global_db = _cursor_home / "User" / "globalStorage" / "state.vscdb"


def _cursor_composer_ids(ws_db: Path) -> list[str]:
    if not ws_db.exists():
        return []
    try:
        conn = sqlite3.connect(str(ws_db))
        cur = conn.cursor()
        cur.execute("SELECT value FROM ItemTable WHERE key = 'composer.composerData'")
        row = cur.fetchone()
        conn.close()
        if not row:
            return []
        data = json.loads(row[0])
        return [c.get("composerId", "") for c in data.get("allComposers", []) if c.get("composerId")]
    except (sqlite3.Error, json.JSONDecodeError, OSError):
        return []


def _cursor_conversation(global_db: Path, composer_id: str) -> list[dict]:
    if not global_db.exists():
        return []
    try:
        conn = sqlite3.connect(str(global_db))
        cur = conn.cursor()
        cur.execute("SELECT value FROM cursorDiskKV WHERE key = ?", (f"composerData:{composer_id}",))
        row = cur.fetchone()
        conn.close()
        if not row:
            return []
        return json.loads(row[0]).get("conversation", [])
    except (sqlite3.Error, json.JSONDecodeError, OSError):
        return []


def _cursor_turns(conversation: list[dict]) -> list[tuple[str, str, str]]:
    """Cursor: type 1=user, 2=assistant."""
    turns: list[tuple[str, str, str]] = []
    cur_user: Optional[str] = None
    for msg in conversation:
        text = str(msg.get("text", "")).strip()
        if msg.get("type") == 1 and text:
            cur_user = text
        elif msg.get("type") == 2 and text and cur_user:
            turns.append((cur_user, text, ""))
            cur_user = None
    return turns


def list_cursor_sessions(project_cwd: str, **_: object) -> list[Session]:
    if not _cursor_global_db.exists() or not _cursor_ws_base.is_dir():
        return []
    project_cwd = project_cwd.rstrip("/")
    results: list[Session] = []
    seen: set[str] = set()
    for ws_dir in sorted(_cursor_ws_base.iterdir()):
        if not ws_dir.is_dir():
            continue
        folder = read_workspace_folder(ws_dir)
        if not folder or not is_subpath(folder.rstrip("/"), project_cwd):
            continue
        for cid in _cursor_composer_ids(ws_dir / "state.vscdb"):
            if cid in seen:
                continue
            seen.add(cid)
            turns = _cursor_turns(_cursor_conversation(_cursor_global_db, cid))
            if turns:
                results.append(Session(id=cid, turns=turns, path=str(ws_dir)))
    return results
