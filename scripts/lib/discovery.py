"""Unified session discovery for all AI coding tools.

Discovers conversation sessions from Claude Code, Cursor, Trae, and Codex
for a specific project. Each tool defines its own home discovery and session
listing logic; shared utilities handle JSONL reading, workspace mapping,
text extraction, and turn pairing.

Tool config is a dict with keys:
    name        — tool identifier ("claude", "cursor", "trae", "codex")
    list_sessions(project_cwd, **kwargs) → list[Session]
"""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Iterator, Optional
from urllib.parse import unquote

from .constants import (
    CODEX_DEFAULT_HOME,
    CODEX_HOME_ENV,
    CODEX_INDEX_REL,
    CODEX_SESSIONS_REL,
)
from .hash_util import content_hash
from .session_writer import create_session_file
from .source_index import append_index
from .time_util import now_iso


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



def _read_jsonl(path: Path) -> list[dict]:
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


def _read_workspace_folder(ws_dir: Path) -> Optional[str]:
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


def _extract_text(content: object, accepted_types: Optional[tuple[str, ...]] = None) -> str:
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


def _is_subpath(child: str, parent: str) -> bool:
    """Check if child equals parent or is a descendant directory."""
    parent = parent.rstrip("/")
    return child == parent or child.startswith(parent + "/")


def _iter_jsonl_files(directory: Path, pattern: str = "*.jsonl", recursive: bool = False) -> Iterator[tuple[Path, str]]:
    """Yield (path, stem) for JSONL files matching *pattern* in *directory*."""
    glob_fn = directory.rglob if recursive else directory.glob
    for p in sorted(glob_fn(pattern)):
        if p.is_file():
            yield p, p.stem


# ---------------------------------------------------------------------------
# Claude Code
# ---------------------------------------------------------------------------

_claude_home = Path("~/.claude").expanduser()


def _claude_project_dirs(project_cwd: str) -> list[Path]:
    """Find all Claude project dirs matching project_cwd and its sub-projects."""
    encoded = project_cwd.replace("/", "-").replace(" ", "-")
    projects_dir = _claude_home / "projects"
    if not projects_dir.is_dir():
        return []
    dirs = []
    for d in sorted(projects_dir.iterdir()):
        if not d.is_dir():
            continue
        if d.name == encoded or d.name.startswith(encoded + "-"):
            dirs.append(d)
    return dirs


def _claude_turns(entries: list[dict]) -> list[tuple[str, str, str]]:
    """Pair Claude Code user/assistant messages into turns.

    Skips meta messages and tool_result (list content) user messages.
    Accumulates multi-part assistant responses.
    """
    turns: list[tuple[str, str, str]] = []
    cur_user: Optional[str] = None
    cur_ts: Optional[str] = None
    cur_answer: list[str] = []

    def _flush() -> None:
        nonlocal cur_user, cur_ts, cur_answer
        if cur_user and cur_answer:
            answer = "\n".join(cur_answer).strip()
            if answer:
                turns.append((cur_user, answer, cur_ts or ""))
        cur_user = cur_ts = None
        cur_answer = []

    for entry in entries:
        if entry.get("type") == "user":
            if entry.get("isMeta"):
                continue
            content = entry.get("message", {}).get("content", "")
            if isinstance(content, str) and content.strip():
                _flush()
                cur_user = content.strip()
                cur_ts = entry.get("timestamp", "")
        elif entry.get("type") == "assistant" and cur_user:
            text = _extract_text(entry.get("message", {}).get("content", ""), accepted_types=("text",))
            if text.strip():
                cur_answer.append(text.strip())

    _flush()
    return turns


def list_claude_sessions(project_cwd: str, **_: object) -> list[Session]:
    sessions_dirs = _claude_project_dirs(project_cwd)
    if not sessions_dirs:
        return []
    results: list[Session] = []
    for sessions_dir in sessions_dirs:
        for path, sid in _iter_jsonl_files(sessions_dir):
            turns = _claude_turns(_read_jsonl(path))
            if turns:
                results.append(Session(id=sid, turns=turns, path=str(path)))
    return results


# ---------------------------------------------------------------------------
# Codex
# ---------------------------------------------------------------------------

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
        text = _extract_text(payload.get("content", []), accepted_types=("input_text", "output_text"))
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
    """Discover the Codex home directory (public API for setup/remove scripts)."""
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
        for entry in _read_jsonl(index_path):
            sid = entry.get("id", "")
            if sid:
                index_map[sid] = entry

    results: list[Session] = []
    for path, stem in _iter_jsonl_files(sessions_dir, "rollout-*.jsonl", recursive=True):
        parts = stem.split("-", 6)
        sid = parts[6] if len(parts) >= 7 else stem

        entries = _read_jsonl(path)
        header = next(
            (e.get("payload", {}) for e in entries if e.get("type") == "session_meta"),
            {},
        )
        if project_cwd and not _is_subpath(header.get("cwd", ""), project_cwd):
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


# ---------------------------------------------------------------------------
# Cursor
# ---------------------------------------------------------------------------

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
        folder = _read_workspace_folder(ws_dir)
        if not folder or not _is_subpath(folder.rstrip("/"), project_cwd):
            continue
        for cid in _cursor_composer_ids(ws_dir / "state.vscdb"):
            if cid in seen:
                continue
            seen.add(cid)
            turns = _cursor_turns(_cursor_conversation(_cursor_global_db, cid))
            if turns:
                results.append(Session(id=cid, turns=turns, path=str(ws_dir)))
    return results


# ---------------------------------------------------------------------------
# Trae / Trae CN
# ---------------------------------------------------------------------------

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
        text = _extract_text(msg.get("content", ""))
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
            folder = _read_workspace_folder(ws_dir)
            if not folder or not _is_subpath(folder.rstrip("/"), project_cwd_norm):
                continue
            for session in _trae_sessions(ws_dir / "state.vscdb"):
                sid = session.get("sessionId", "")
                turns = _trae_turns(session.get("messages", []))
                if turns:
                    results.append(Session(id=sid, turns=turns, path=str(ws_dir)))
    return results


# ---------------------------------------------------------------------------
# Unified discovery
# ---------------------------------------------------------------------------

TOOL_CONFIGS: dict[str, dict] = {
    "claude": {"name": "claude", "list_sessions": list_claude_sessions},
    "codex": {"name": "codex", "list_sessions": list_codex_sessions},
    "cursor": {"name": "cursor", "list_sessions": list_cursor_sessions},
    "trae": {"name": "trae", "list_sessions": list_trae_sessions},
}

TOOL_PREFIX = {
    "claude": "session-claude",
    "cursor": "session-cursor",
    "trae": "session-trae",
    "codex": "session-codex",
}


def discover_sessions(
    project_cwd: str,
    tools: Optional[list[str]] = None,
    **kwargs: object,
) -> dict[str, list[Session]]:
    """Discover sessions from all (or specified) tools for a project.

    Returns {tool_name: [Session, ...]}.
    Extra kwargs are forwarded to each tool's list_sessions (e.g. since=).
    """
    if tools is None:
        tools = list(TOOL_CONFIGS.keys())
    results: dict[str, list[Session]] = {}
    for tool in tools:
        cfg = TOOL_CONFIGS.get(tool)
        if not cfg:
            continue
        try:
            results[tool] = cfg["list_sessions"](project_cwd, **kwargs)
        except Exception:
            results[tool] = []
    return results


# ---------------------------------------------------------------------------
# Session file writing (used by scan-all-sessions.py)
# ---------------------------------------------------------------------------

def session_filename(tool: str, session_id: str) -> str:
    """Generate session filename: session-{tool}-{id}.md"""
    prefix = TOOL_PREFIX.get(tool, f"session-{tool}")
    safe_id = session_id.replace("/", "-").replace("\\", "-")[:80]
    return f"{prefix}-{safe_id}.md"


def combined_hash(turns: list[tuple[str, str, str]]) -> str:
    """Compute content hash for a session's combined turns."""
    combined = "\n---\n".join(f"{u}\n---\n{a}" for u, a, _ in turns)
    return content_hash(combined)


def write_session(
    tool: str,
    session: Session,
    collect_root: Path,
    indexed_paths: set[str],
) -> bool:
    """Write a session to disk if not already captured. Returns True if written."""
    if not session.turns:
        return False

    filename = session_filename(tool, session.id)
    sessions_dir = collect_root / "active" / "sessions"
    session_file = sessions_dir / filename
    rel_path = str(session_file.relative_to(collect_root))

    if session_file.exists():
        return False

    c_hash = combined_hash(session.turns)
    if rel_path in indexed_paths:
        return False

    source_id = f"scan-{tool}-{session.id}"
    turns_2 = [(u, a) for u, a, _ in session.turns]
    create_session_file(
        sessions_dir=sessions_dir,
        source_id=source_id,
        agent=tool,
        session_id=session.id,
        turns=turns_2,
        filename=filename,
    )

    append_index(collect_root, {
        "source_id": source_id,
        "source_time": now_iso(),
        "source_type": "agent_conversation_turn",
        "source_channel": "active",
        "path": rel_path,
        "content_hash": c_hash,
        "metadata_status": "complete",
        "noise_hint": "none",
        "status": "collected",
    })

    return True
