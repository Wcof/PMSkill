"""Unified session discovery for all AI coding tools.

Discovers conversation sessions from Claude Code, Cursor, Trae, and Codex
for a specific project. This module is a thin entry point that delegates
to tool-specific adapter modules.

Tool config is a dict with keys:
    name        — tool identifier ("claude", "cursor", "trae", "codex")
    list_sessions(project_cwd, **kwargs) → list[Session]
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .discovery_claude import list_claude_sessions
from .discovery_codex import _codex_turns  # re-export for tests
from .discovery_codex import find_codex_home as _find_codex_home
from .discovery_codex import list_codex_sessions
from .discovery_cursor import list_cursor_sessions
from .discovery_shared import (
    Session,
    extract_text,
    is_subpath,
    iter_jsonl_files,
    read_jsonl,
    read_workspace_folder,
)
from .discovery_trae import list_trae_sessions
from .hash_util import content_hash
from .session_writer import create_session_file
from .source_index import append_index
from .time_util import now_iso


# Re-export commonly used shared symbols
# (used by tests and external callers)
_read_jsonl = read_jsonl
_read_workspace_folder = read_workspace_folder
_extract_text = extract_text
_is_subpath = is_subpath
_iter_jsonl_files = iter_jsonl_files

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


def find_codex_home() -> Path:
    """Discover the Codex home directory."""
    return _find_codex_home()


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
    rel_path = session_file.relative_to(collect_root).as_posix()

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
