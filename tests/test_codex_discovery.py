"""Tests for scripts/lib/codex_discovery.py."""

import json
import os
from pathlib import Path

from scripts.lib.codex_discovery import (
    filter_turns,
    find_codex_home,
    find_session_index,
    find_sessions_dir,
    iter_session_files,
    list_project_sessions,
    parse_session_header,
    parse_session_index,
    parse_session_jsonl,
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


def test_find_codex_home_default(tmp_path: Path):
    """Default home should be ~/.codex."""
    # Clear env var if set
    os.environ.pop("CODEX_HOME", None)
    home = find_codex_home()
    assert home == Path("~/.codex").expanduser()


def test_find_codex_home_env(tmp_path: Path, monkeypatch):
    """CODEX_HOME env var should override default."""
    custom = tmp_path / "custom-codex"
    monkeypatch.setenv("CODEX_HOME", str(custom))
    home = find_codex_home()
    assert home == custom.resolve()


def test_find_session_index(tmp_path: Path):
    """Should find session_index.jsonl if it exists."""
    codex_home = tmp_path / "codex"
    codex_home.mkdir()
    index = codex_home / "session_index.jsonl"
    index.write_text('{"id":"test"}\n', encoding="utf-8")
    assert find_session_index(codex_home) == index


def test_find_session_index_missing(tmp_path: Path):
    """Should return None if session_index.jsonl doesn't exist."""
    codex_home = tmp_path / "codex"
    codex_home.mkdir()
    assert find_session_index(codex_home) is None


def test_find_sessions_dir(tmp_path: Path):
    """Should find sessions directory."""
    codex_home = tmp_path / "codex"
    (codex_home / "sessions").mkdir(parents=True)
    assert find_sessions_dir(codex_home) == codex_home / "sessions"


def test_parse_session_index(tmp_path: Path):
    """Should parse session_index.jsonl correctly."""
    codex_home = tmp_path / "codex"
    codex_home.mkdir()
    index = codex_home / "session_index.jsonl"
    entries = [
        {"id": "s1", "thread_name": "测试会话1", "updated_at": "2026-05-01T10:00:00Z"},
        {"id": "s2", "thread_name": "测试会话2", "updated_at": "2026-05-01T11:00:00Z"},
    ]
    _write_jsonl(index, entries)
    result = parse_session_index(codex_home)
    assert len(result) == 2
    assert result[0]["id"] == "s1"


def test_parse_session_jsonl(tmp_path: Path):
    """Should parse a session JSONL file correctly."""
    jsonl = tmp_path / "rollout-test.jsonl"
    entries = _make_session_entries()
    _write_jsonl(jsonl, entries)
    result = parse_session_jsonl(jsonl)
    assert len(result) == 5
    assert result[0]["type"] == "session_meta"


def test_filter_turns():
    """Should extract user/assistant message pairs."""
    entries = _make_session_entries()
    turns = filter_turns(entries)
    assert len(turns) == 2
    assert turns[0][0] == "你好，帮我设计一个登录页面"
    assert turns[0][1] == "好的，我来设计一个登录页面..."
    assert turns[1][0] == "加上验证码功能"


def test_filter_turns_since():
    """Should filter turns by timestamp."""
    entries = _make_session_entries()
    # Only include turns after 10:01:30
    turns = filter_turns(entries, since="2026-05-01T10:01:30Z")
    assert len(turns) == 1
    assert turns[0][0] == "加上验证码功能"


def test_filter_turns_no_assistant():
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
    turns = filter_turns(entries)
    assert len(turns) == 0


def test_list_project_sessions(tmp_path: Path):
    """Should list sessions matching a project cwd."""
    codex_home = tmp_path / "codex"
    sessions_dir = codex_home / "sessions" / "2026" / "05" / "01"
    sessions_dir.mkdir(parents=True)

    # Write session index
    index = codex_home / "session_index.jsonl"
    _write_jsonl(index, [
        {"id": "019de2d9-aee9-7c12-ade9-a66988645a37", "thread_name": "测试", "updated_at": "2026-05-01T10:00:00Z"},
    ])

    # Write session JSONL
    entries = _make_session_entries(project_cwd="/test/project")
    jsonl = sessions_dir / "rollout-2026-05-01T10-00-00-019de2d9-aee9-7c12-ade9-a66988645a37.jsonl"
    _write_jsonl(jsonl, entries)

    result = list_project_sessions(codex_home, "/test/project")
    assert len(result) == 1
    assert result[0]["id"] == "019de2d9-aee9-7c12-ade9-a66988645a37"
    assert result[0]["thread_name"] == "测试"
    assert len(result[0]["turns"]) == 2


def test_list_project_sessions_no_match(tmp_path: Path):
    """Should return empty if no sessions match the project."""
    codex_home = tmp_path / "codex"
    sessions_dir = codex_home / "sessions" / "2026" / "05" / "01"
    sessions_dir.mkdir(parents=True)

    entries = _make_session_entries(project_cwd="/other/project")
    jsonl = sessions_dir / "rollout-2026-05-01T10-00-00-019de2d9-aee9-7c12-ade9-a66988645a37.jsonl"
    _write_jsonl(jsonl, entries)

    result = list_project_sessions(codex_home, "/test/project")
    assert len(result) == 0


def test_parse_session_header(tmp_path: Path):
    """Should read only session_meta payload without loading full file."""
    jsonl = tmp_path / "rollout-test.jsonl"
    entries = _make_session_entries()
    _write_jsonl(jsonl, entries)
    header = parse_session_header(jsonl)
    assert header["id"] == "test-session-001"
    assert header["cwd"] == "/test/project"


def test_parse_session_header_no_meta(tmp_path: Path):
    """Should return empty dict if no session_meta entry exists."""
    jsonl = tmp_path / "rollout-test.jsonl"
    _write_jsonl(jsonl, [
        {"timestamp": "2026-05-01T10:01:00Z", "type": "response_item", "payload": {"type": "message", "role": "user", "content": []}},
    ])
    header = parse_session_header(jsonl)
    assert header == {}


def test_iter_session_files(tmp_path: Path):
    """Should discover session JSONL files and extract session IDs."""
    sessions_dir = tmp_path / "sessions" / "2026" / "05" / "01"
    sessions_dir.mkdir(parents=True)
    uuid = "019de2d9-aee9-7c12-ade9-a66988645a37"
    jsonl = sessions_dir / f"rollout-2026-05-01T10-00-00-{uuid}.jsonl"
    _write_jsonl(jsonl, [{"type": "session_meta", "payload": {}}])

    results = list(iter_session_files(tmp_path / "sessions"))
    assert len(results) == 1
    assert results[0][0] == jsonl
    assert results[0][1] == uuid


def test_iter_session_files_nested(tmp_path: Path):
    """Should find files in nested date directories."""
    sessions_dir = tmp_path / "sessions" / "2026" / "05" / "02"
    sessions_dir.mkdir(parents=True)
    uuid = "aabbccdd-1111-2222-3333-444455556666"
    jsonl = sessions_dir / f"rollout-2026-05-02T12-00-00-{uuid}.jsonl"
    _write_jsonl(jsonl, [{"type": "session_meta", "payload": {}}])

    results = list(iter_session_files(tmp_path / "sessions"))
    assert len(results) == 1
    assert results[0][1] == uuid
