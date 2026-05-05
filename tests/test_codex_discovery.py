"""Tests for scripts/lib/discovery.py — Codex session discovery."""

import json
from pathlib import Path

from scripts.lib.discovery import (
    _codex_turns,
    _iter_jsonl_files,
    _read_jsonl,
    find_codex_home,
    list_codex_sessions,
)


def _write_jsonl(path: Path, entries: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(e, ensure_ascii=False) for e in entries]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _make_session_entries(project_cwd: str = "/test/project", with_turns: bool = True) -> list[dict]:
    entries = [
        {
            "timestamp": "2026-05-01T10:00:00Z",
            "type": "session_meta",
            "payload": {
                "id": "test-session-001",
                "cwd": project_cwd,
                "timestamp": "2026-05-01T10:00:00Z",
            },
        },
    ]
    if with_turns:
        entries.extend([
            {
                "timestamp": "2026-05-01T10:01:00Z",
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"type": "input_text", "text": "你好，帮我设计一个登录页面"}],
                },
            },
            {
                "timestamp": "2026-05-01T10:01:30Z",
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": "好的，我来设计一个登录页面..."}],
                },
            },
            {
                "timestamp": "2026-05-01T10:02:00Z",
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "user",
                    "content": [{"type": "input_text", "text": "加上验证码功能"}],
                },
            },
            {
                "timestamp": "2026-05-01T10:02:30Z",
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": "好的，验证码功能已添加..."}],
                },
            },
        ])
    return entries


def test_find_codex_home():
    """find_codex_home returns a resolved Path."""
    home = find_codex_home()
    assert isinstance(home, Path)
    assert home == home.resolve()


def test_read_jsonl(tmp_path: Path):
    """Should parse a JSONL file and return all valid entries."""
    jsonl = tmp_path / "test.jsonl"
    entries = _make_session_entries()
    _write_jsonl(jsonl, entries)
    result = _read_jsonl(jsonl)
    assert len(result) == 5
    assert result[0]["type"] == "session_meta"


def test_codex_turns():
    """Should extract user/assistant message pairs."""
    entries = _make_session_entries()
    turns = _codex_turns(entries)
    assert len(turns) == 2
    assert turns[0][0] == "你好，帮我设计一个登录页面"
    assert turns[0][1] == "好的，我来设计一个登录页面..."
    assert turns[1][0] == "加上验证码功能"


def test_codex_turns_since():
    """Should filter turns by timestamp."""
    entries = _make_session_entries()
    turns = _codex_turns(entries, since="2026-05-01T10:01:30Z")
    assert len(turns) == 1
    assert turns[0][0] == "加上验证码功能"


def test_codex_turns_no_assistant():
    """Should not return incomplete pairs (user without assistant)."""
    entries = [
        {
            "timestamp": "2026-05-01T10:00:00Z",
            "type": "session_meta",
            "payload": {"id": "s1", "cwd": "/test"},
        },
        {
            "timestamp": "2026-05-01T10:01:00Z",
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "问题"}],
            },
        },
    ]
    turns = _codex_turns(entries)
    assert len(turns) == 0


def test_list_codex_sessions(tmp_path: Path):
    """Should list sessions matching a project cwd."""
    sessions_dir = tmp_path / "sessions" / "2026" / "05" / "01"
    sessions_dir.mkdir(parents=True)

    # Write session index
    index = tmp_path / "session_index.jsonl"
    _write_jsonl(index, [
        {"id": "019de2d9-aee9-7c12-ade9-a66988645a37", "thread_name": "测试", "updated_at": "2026-05-01T10:00:00Z"},
    ])

    # Write session JSONL
    entries = _make_session_entries(project_cwd="/test/project")
    jsonl = sessions_dir / "rollout-2026-05-01T10-00-00-019de2d9-aee9-7c12-ade9-a66988645a37.jsonl"
    _write_jsonl(jsonl, entries)

    result = list_codex_sessions("/test/project", codex_home=tmp_path)
    assert len(result) == 1
    assert result[0].id == "019de2d9-aee9-7c12-ade9-a66988645a37"
    assert result[0].name == "测试"
    assert len(result[0].turns) == 2


def test_list_codex_sessions_no_match(tmp_path: Path):
    """Should return empty if no sessions match the project."""
    sessions_dir = tmp_path / "sessions" / "2026" / "05" / "01"
    sessions_dir.mkdir(parents=True)

    entries = _make_session_entries(project_cwd="/other/project")
    jsonl = sessions_dir / "rollout-2026-05-01T10-00-00-019de2d9-aee9-7c12-ade9-a66988645a37.jsonl"
    _write_jsonl(jsonl, entries)

    result = list_codex_sessions("/test/project", codex_home=tmp_path)
    assert len(result) == 0



def test_iter_jsonl_files(tmp_path: Path):
    """Should discover JSONL files and yield (path, stem) pairs."""
    sessions_dir = tmp_path / "sessions" / "2026" / "05" / "01"
    sessions_dir.mkdir(parents=True)
    uuid = "019de2d9-aee9-7c12-ade9-a66988645a37"
    jsonl = sessions_dir / f"rollout-2026-05-01T10-00-00-{uuid}.jsonl"
    _write_jsonl(jsonl, [{"type": "session_meta", "payload": {}}])

    results = list(_iter_jsonl_files(tmp_path / "sessions", "rollout-*.jsonl", recursive=True))
    assert len(results) == 1
    assert results[0][0] == jsonl
    assert results[0][1] == f"rollout-2026-05-01T10-00-00-{uuid}"


def test_iter_jsonl_files_nested(tmp_path: Path):
    """Should find files in nested date directories."""
    sessions_dir = tmp_path / "sessions" / "2026" / "05" / "02"
    sessions_dir.mkdir(parents=True)
    uuid = "aabbccdd-1111-2222-3333-444455556666"
    jsonl = sessions_dir / f"rollout-2026-05-02T12-00-00-{uuid}.jsonl"
    _write_jsonl(jsonl, [{"type": "session_meta", "payload": {}}])

    results = list(_iter_jsonl_files(tmp_path / "sessions", "rollout-*.jsonl", recursive=True))
    assert len(results) == 1
    assert uuid in results[0][1]
