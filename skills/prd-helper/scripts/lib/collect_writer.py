"""Unified writer for Collect sources."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import re

from .discovery_shared import Session
from .hash_util import content_hash, file_hash
from .metadata import metadata_status_for_text
from .session_writer import append_turn, create_session_file
from .source_index import append_index, append_index_entries, read_indexed_hashes_by_path
from .state import read_collect_state, safe_int, write_collect_state
from .time_util import TZ, now_id, now_iso


SUPPORTED_PASSIVE_EXTENSIONS = {
    ".md": "markdown",
    ".txt": "text",
    ".docx": "word",
    ".pdf": "pdf",
    ".doc": "word",
    ".csv": "csv",
    ".json": "json",
    ".html": "html",
    ".htm": "html",
}


@dataclass(frozen=True)
class CollectWriteResult:
    written: bool
    source_id: str = ""
    rel_path: str = ""
    content_hash: str = ""
    reason: str = ""


@dataclass(frozen=True)
class PassiveScanResult:
    added_count: int
    entries: list[dict] = field(default_factory=list)


def detect_noise(user_query: str, agent_answer: str) -> tuple[str, str]:
    combined = user_query.strip()
    noise_patterns = [
        (r"^(好的|嗯嗯|继续|ok|okay|yes|是的|对的|知道了)\s*[。.!?！？]*$", "possible_noise"),
        (r"^\s*$", "possible_noise"),
    ]
    for pattern, hint in noise_patterns:
        if re.match(pattern, combined, re.IGNORECASE):
            return hint, "短回复或空内容，可能是噪音"
    return "none", ""


def _turn_hash(user_query: str, agent_answer: str) -> str:
    return content_hash(user_query + "\n---\n" + agent_answer)


def _combined_session_hash(turns: list[tuple[str, str, str]]) -> str:
    combined = "\n---\n".join(f"{user}\n---\n{answer}" for user, answer, _ in turns)
    return content_hash(combined)


def _index_entry(
    *,
    source_id: str,
    source_type: str,
    source_channel: str,
    rel_path: str,
    c_hash: str,
    metadata_status: str = "complete",
    noise_hint: str = "none",
) -> dict:
    return {
        "source_id": source_id,
        "source_time": now_iso(),
        "source_type": source_type,
        "source_channel": source_channel,
        "path": rel_path,
        "content_hash": c_hash,
        "metadata_status": metadata_status,
        "noise_hint": noise_hint,
        "status": "collected",
    }


def capture_active_turn(root: Path, agent: str, user_query: str, agent_answer: str) -> CollectWriteResult:
    state = read_collect_state(root)
    if not state:
        return CollectWriteResult(False, reason="collect-state.md not found")
    if state.get("capture_mode") != "on":
        return CollectWriteResult(False, reason=f"capture mode is {state.get('capture_mode', 'off')}")
    if not user_query.strip() and not agent_answer.strip():
        return CollectWriteResult(False, reason="empty turn")

    ts = now_id()
    session_id = state.get("session_id", "unknown")
    turn_index = safe_int(state.get("turn_count")) + 1
    source_id = f"turn-{ts}-{str(turn_index).zfill(3)}"
    c_hash = _turn_hash(user_query, agent_answer)
    noise_hint, noise_reason = detect_noise(user_query, agent_answer)

    sessions_dir = root / "active" / "sessions"
    session_file = sessions_dir / f"session-{session_id}.md"
    if session_file.exists():
        append_turn(session_file, turn_index, user_query, agent_answer)
    else:
        create_session_file(
            sessions_dir=sessions_dir,
            source_id=source_id,
            agent=agent,
            session_id=session_id,
            turns=[(user_query, agent_answer)],
            extra_fields={
                "turn_index": str(turn_index),
                "content_hash": c_hash,
                "noise_hint": noise_hint,
                "noise_reason": noise_reason,
            },
        )

    rel_path = session_file.relative_to(root).as_posix()
    state["turn_count"] = str(turn_index)
    state["last_collect_at"] = now_iso()
    state["last_source_id"] = source_id
    state["last_content_hash"] = c_hash
    state["last_write_file"] = str(session_file)
    state["active_source_count"] = str(safe_int(state.get("active_source_count")) + 1)
    state["total_sources"] = str(safe_int(state.get("total_sources")) + 1)
    if noise_hint == "possible_noise":
        state["possible_noise_count"] = str(safe_int(state.get("possible_noise_count")) + 1)
    write_collect_state(root, state)

    append_index(
        root,
        _index_entry(
            source_id=source_id,
            source_type="agent_conversation_turn",
            source_channel="active",
            rel_path=rel_path,
            c_hash=c_hash,
            metadata_status="complete",
            noise_hint=noise_hint,
        ),
    )

    return CollectWriteResult(True, source_id, rel_path, c_hash)


def session_filename(tool: str, session_id: str) -> str:
    safe_id = session_id.replace("/", "-").replace("\\", "-")[:80]
    return f"session-{tool}-{safe_id}.md"


def capture_historical_session(
    tool: str,
    session: Session,
    collect_root: Path,
    indexed_paths: set[str],
) -> CollectWriteResult:
    if not session.turns:
        return CollectWriteResult(False, reason="empty session")

    filename = session_filename(tool, session.id)
    sessions_dir = collect_root / "active" / "sessions"
    session_file = sessions_dir / filename
    rel_path = session_file.relative_to(collect_root).as_posix()
    if session_file.exists() or rel_path in indexed_paths:
        return CollectWriteResult(False, rel_path=rel_path, reason="already captured")

    c_hash = _combined_session_hash(session.turns)
    source_id = f"scan-{tool}-{session.id}"
    turns = [(user, answer) for user, answer, _ in session.turns]
    create_session_file(
        sessions_dir=sessions_dir,
        source_id=source_id,
        agent=tool,
        session_id=session.id,
        turns=turns,
        filename=filename,
        extra_fields={"content_hash": c_hash},
    )
    append_index(
        collect_root,
        _index_entry(
            source_id=source_id,
            source_type="agent_conversation_turn",
            source_channel="active",
            rel_path=rel_path,
            c_hash=c_hash,
        ),
    )
    return CollectWriteResult(True, source_id, rel_path, c_hash)


def _passive_metadata_status(path: Path) -> str:
    if path.suffix.lower() not in (".md", ".txt"):
        return "missing"
    try:
        return metadata_status_for_text(path.read_text(encoding="utf-8"))
    except Exception:
        return "missing"


def passive_entry(root: Path, path: Path, c_hash: str | None = None) -> dict:
    c_hash = c_hash or file_hash(path)
    rel_path = path.relative_to(root).as_posix()
    source_type = SUPPORTED_PASSIVE_EXTENSIONS.get(path.suffix.lower(), "unknown")
    safe_stem = path.stem.replace("/", "-").replace("\\", "-")
    source_id = f"passive-{safe_stem}-{datetime.now(TZ).strftime('%Y%m%d')}-{c_hash.removeprefix('sha256:')}"
    return _index_entry(
        source_id=source_id,
        source_type=source_type,
        source_channel="passive",
        rel_path=rel_path,
        c_hash=c_hash,
        metadata_status=_passive_metadata_status(path),
    )


def scan_passive_sources(root: Path) -> PassiveScanResult:
    passive_dir = root / "passive"
    passive_dir.mkdir(parents=True, exist_ok=True)
    state = read_collect_state(root)
    indexed_hashes = read_indexed_hashes_by_path(root)
    entries: list[dict] = []

    for path in sorted(passive_dir.rglob("*")):
        if path.is_dir():
            continue
        rel_path = path.relative_to(root).as_posix()
        c_hash = file_hash(path)
        if c_hash in indexed_hashes.get(rel_path, set()):
            continue
        entries.append(passive_entry(root, path, c_hash))

    added_count = append_index_entries(root, entries)
    if added_count > 0:
        state["passive_source_count"] = str(safe_int(state.get("passive_source_count")) + added_count)
        state["total_sources"] = str(safe_int(state.get("total_sources")) + added_count)
        write_collect_state(root, state)
    return PassiveScanResult(added_count=added_count, entries=entries[:added_count])
