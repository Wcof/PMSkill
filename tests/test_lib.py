from pathlib import Path

from scripts.lib.hash_util import content_hash, file_hash
from scripts.lib.id_registry import ALL_ENTITIES, ENTITY_BY_PREFIX, entity_pattern
from scripts.lib.metadata import metadata_status_for_text
from scripts.lib.source_index import (
    append_index,
    append_index_entries,
    ensure_index,
    indexed_hashes_by_path_from_content,
    indexed_paths_from_content,
    read_indexed_paths,
)
from scripts.lib.state import read_collect_state, write_collect_state


def test_collect_state_round_trip(tmp_path: Path):
    state = {
        "capture_mode": "on",
        "session_id": "prd-session-test",
        "turn_count": "3",
        "custom_key": "custom_value",
    }

    write_collect_state(tmp_path, state)

    assert read_collect_state(tmp_path)["capture_mode"] == "on"
    assert read_collect_state(tmp_path)["session_id"] == "prd-session-test"
    assert read_collect_state(tmp_path)["custom_key"] == "custom_value"


def test_source_index_append_and_read_paths(tmp_path: Path):
    ensure_index(tmp_path)
    append_index(
        tmp_path,
        {
            "source_id": "turn-001",
            "source_time": "2026-05-02T10:00:00+08:00",
            "source_type": "agent_conversation_turn",
            "source_channel": "active",
            "path": "active/sessions/session-test.md",
            "content_hash": "sha256:abc",
            "metadata_status": "complete",
            "noise_hint": "none",
            "status": "collected",
        },
    )
    append_index(
        tmp_path,
        {
            "source_id": "turn-002",
            "source_time": "2026-05-02T10:05:00+08:00",
            "source_type": "agent_conversation_turn",
            "source_channel": "active",
            "path": "active/sessions/session-test.md",
            "content_hash": "sha256:def",
            "metadata_status": "complete",
            "noise_hint": "none",
            "status": "collected",
        },
    )
    # Same source_id again — should be deduplicated
    append_index(
        tmp_path,
        {
            "source_id": "turn-002",
            "source_time": "2026-05-02T10:05:00+08:00",
            "source_type": "agent_conversation_turn",
            "source_channel": "active",
            "path": "active/sessions/session-test.md",
            "content_hash": "sha256:def",
            "metadata_status": "complete",
            "noise_hint": "none",
            "status": "collected",
        },
    )

    # Same session file appears twice (two turns), but same source_id only once
    assert "active/sessions/session-test.md" in read_indexed_paths(tmp_path)
    content = (tmp_path / "source-index.md").read_text(encoding="utf-8")
    assert content.count("active/sessions/session-test.md") == 2
    assert content.count("turn-002") == 1


def test_source_index_uses_shared_markdown_table_parser():
    content = """
# Source Index

| source_id | source_time | source_type | source_channel | path | content_hash | metadata_status | noise_hint | status |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| source_001 | 2026-05-03 | markdown | passive | passive/meeting.md | sha256:abc | complete | none | collected |
"""

    assert indexed_paths_from_content(content) == {"passive/meeting.md"}


def test_source_index_batch_append_reads_existing_ids_once(tmp_path: Path):
    ensure_index(tmp_path)
    added = append_index_entries(
        tmp_path,
        [
            {
                "source_id": "turn-001",
                "source_time": "2026-05-02T10:00:00+08:00",
                "source_type": "agent_conversation_turn",
                "source_channel": "active",
                "path": "active/sessions/session-test.md",
                "content_hash": "sha256:abc",
                "metadata_status": "complete",
                "noise_hint": "none",
                "status": "collected",
            },
            {
                "source_id": "turn-001",
                "source_time": "2026-05-02T10:00:00+08:00",
                "source_type": "agent_conversation_turn",
                "source_channel": "active",
                "path": "active/sessions/session-test.md",
                "content_hash": "sha256:abc",
                "metadata_status": "complete",
                "noise_hint": "none",
                "status": "collected",
            },
        ],
    )

    content = (tmp_path / "source-index.md").read_text(encoding="utf-8")
    assert added == 1
    assert content.count("turn-001") == 1
    assert indexed_hashes_by_path_from_content(content) == {
        "active/sessions/session-test.md": {"sha256:abc"}
    }


def test_hash_util_is_consistent(tmp_path: Path):
    text = "hello prd helper"
    path = tmp_path / "source.txt"
    path.write_text(text, encoding="utf-8")

    assert content_hash(text) == file_hash(path)
    assert content_hash(text).startswith("sha256:")


def test_id_registry_entities_are_complete():
    prefixes = {entity.prefix for entity in ALL_ENTITIES}

    assert {"fact", "decision", "constraint", "page", "feature", "rule", "data", "acceptance"} <= prefixes
    assert set(ENTITY_BY_PREFIX) == prefixes
    assert "fact_001" in ENTITY_BY_PREFIX["fact"].extract_ids("fact_001")
    assert entity_pattern()
    assert ("generate", "作为生成文档的事实、约束、问题或推断依据") in ENTITY_BY_PREFIX["fact"].lifecycle
    assert ("relate", "创建关系实体并连接 fact/page/feature/rule/data/acceptance 链路") in ENTITY_BY_PREFIX["rule"].lifecycle


def test_bilingual_metadata_detection():
    chinese = """
- 来源：会议纪要
- 记录时间：2026-05-02
- 记录人：产品经理
- 责任人：业务负责人
- 优先级：高
"""
    english = """
source: meeting notes
source_time: 2026-05-02
recorder: product manager
owner: business owner
priority: high
"""
    partial = """
- 来源：会议纪要
- 记录时间：2026-05-02
"""
    missing = """
- 一些无关内容
"""

    source_type_only = """
- 材料类型：会议纪要
"""
    core_with_type = """
- 来源：会议纪要
- 记录时间：2026-05-02
- 材料类型：meeting
"""

    assert metadata_status_for_text(chinese) == "complete"
    assert metadata_status_for_text(english) == "complete"
    assert metadata_status_for_text(partial) == "partial"
    assert metadata_status_for_text(missing) == "missing"
    assert metadata_status_for_text(source_type_only) == "missing"
    assert metadata_status_for_text(core_with_type) == "partial"

