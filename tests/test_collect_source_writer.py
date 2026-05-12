from pathlib import Path

from scripts.lib.collect_writer import (
    capture_active_turn,
    capture_historical_session,
    scan_passive_sources,
)
from scripts.lib.discovery_shared import Session
from scripts.lib.source_index import read_indexed_paths
from scripts.lib.state import read_collect_state, write_collect_state


def test_collect_source_writer_captures_active_turn_and_updates_state(tmp_path: Path):
    root = tmp_path / "01-collect"
    root.mkdir()
    write_collect_state(
        root,
        {
            "capture_mode": "on",
            "session_id": "session-001",
            "turn_count": "0",
            "active_source_count": "0",
            "total_sources": "0",
            "possible_noise_count": "0",
        },
    )

    result = capture_active_turn(
        root=root,
        agent="codex",
        user_query="我们需要机器人巡检点位管理。",
        agent_answer="已记录这个需求。",
    )

    assert result.written
    assert result.source_id.startswith("turn-")
    assert result.rel_path == "active/sessions/session-session-001.md"
    assert "机器人巡检点位管理" in (root / result.rel_path).read_text(encoding="utf-8")
    state = read_collect_state(root)
    assert state["turn_count"] == "1"
    assert state["active_source_count"] == "1"
    assert state["total_sources"] == "1"
    assert result.rel_path in read_indexed_paths(root)


def test_collect_source_writer_captures_historical_session_once(tmp_path: Path):
    root = tmp_path / "01-collect"
    session = Session(
        id="history-001",
        turns=[("用户问题", "Agent 回答", "Turn 1")],
    )

    first = capture_historical_session("codex", session, root, read_indexed_paths(root))
    second = capture_historical_session("codex", session, root, read_indexed_paths(root))

    assert first.written
    assert not second.written
    assert first.rel_path == "active/sessions/session-codex-history-001.md"
    assert first.rel_path in read_indexed_paths(root)


def test_collect_source_writer_indexes_passive_sources_once_per_hash(tmp_path: Path):
    root = tmp_path / "01-collect"
    passive = root / "passive"
    passive.mkdir(parents=True)
    source = passive / "meeting.md"
    source.write_text("- 来源：会议纪要\n- 记录时间：2026-05-03\n", encoding="utf-8")
    write_collect_state(root, {"passive_source_count": "0", "total_sources": "0"})

    first = scan_passive_sources(root)
    second = scan_passive_sources(root)
    source.write_text("- 来源：会议纪要\n- 记录时间：2026-05-04\n", encoding="utf-8")
    third = scan_passive_sources(root)

    assert first.added_count == 1
    assert second.added_count == 0
    assert third.added_count == 1
    state = read_collect_state(root)
    assert state["passive_source_count"] == "2"
    assert state["total_sources"] == "2"
