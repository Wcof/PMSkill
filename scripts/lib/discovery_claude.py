"""Claude Code session discovery adapter."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .discovery_shared import (
    Session,
    extract_text,
    iter_jsonl_files,
    read_jsonl,
)


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
            text = extract_text(entry.get("message", {}).get("content", ""), accepted_types=("text",))
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
        for path, sid in iter_jsonl_files(sessions_dir):
            turns = _claude_turns(read_jsonl(path))
            if turns:
                results.append(Session(id=sid, turns=turns, path=str(path)))
    return results
