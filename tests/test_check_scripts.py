import importlib.util
from pathlib import Path

from scripts.lib.source_index import append_index, ensure_index
from scripts.lib.state import write_collect_state


ROOT = Path(__file__).resolve().parents[1]


def load_script(relative_path: str):
    path = ROOT / relative_path
    name = Path(relative_path).name
    spec = importlib.util.spec_from_file_location(name.replace("-", "_").removesuffix(".py"), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write(path: Path, content: str = "content") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def test_check_collect_writes_template_shaped_check(tmp_path: Path):
    root = tmp_path / "01-collect"
    write(root / "active" / "sessions" / "turn-001.md", "---\nsource_id: turn-001\n---\nUser Query\nAgent Answer\n")
    write(root / "passive" / "meeting.md", "- 来源：会议\n")
    write_collect_state(
        root,
        {
            "capture_mode": "off",
            "started_at": "2026-05-02T10:00:00+08:00",
            "active_source_count": "1",
            "passive_source_count": "1",
            "turn_count": "1",
        },
    )
    ensure_index(root)
    append_index(
        root,
        {
            "source_id": "turn-001",
            "source_time": "2026-05-02T10:00:00+08:00",
            "source_type": "agent_conversation_turn",
            "source_channel": "active",
            "path": "active/sessions/turn-001.md",
            "content_hash": "sha256:abc",
            "metadata_status": "complete",
            "noise_hint": "none",
            "status": "collected",
        },
    )

    module = load_script("modules/collect/scripts/check-collect.py")
    result = module.check(root)
    check_file = module.write_check_md(root, result)
    content = check_file.read_text()

    assert "## 0. 检查信息" in content
    assert "## 5. 采集结论" in content
    assert "检查状态：通过" in content


def test_check_refine_writes_template_shaped_check(tmp_path: Path):
    root = tmp_path / "prd-helper"
    refine = root / "02-refine"
    write(refine / "background.md", "## 背景\n")
    write(refine / "facts.md", "## fact_001\n- 来源材料：访谈\n- 来源位置：L1\n- 状态：confirmed\n")
    write(refine / "decisions.md", "## decision_001\n- 来源材料：评审\n- 来源位置：L2\n- 状态：confirmed\n")
    write(refine / "constraints.md", "## constraint_001\n- 来源材料：评审\n- 来源位置：L3\n- 状态：confirmed\n")
    write(refine / "goals.md", "## goal_001\n- 来源材料：访谈\n- 状态：confirmed\n")
    write(refine / "conflicts.md", "## conflict_001\n- 涉及来源：客户反馈\n- 当前状态：open\n")
    write(refine / "questions.md", "## question_001\n- 来源材料：访谈\n- 状态：open\n")
    write(refine / "assumptions.md", "## assumption_001\n- 来源材料：访谈\n")

    module = load_script("modules/refine/scripts/check-refine.py")
    result = module.check_refine(root)
    check_file = module.write_check(root, result)
    content = check_file.read_text()

    assert "## 1. 信息分类检查" in content
    assert "已区分需求事实" in content
    assert "本轮精炼是否可以进入关联阶段" in content


def test_check_relate_writes_template_shaped_check(tmp_path: Path):
    root = tmp_path / "prd-helper"
    refine = root / "02-refine"
    relate = root / "03-relate"
    write(refine / "facts.md", "## fact_001\n")
    write(refine / "questions.md", "## question_001\n")
    write(refine / "conflicts.md", "## conflict_001\n")
    write(refine / "assumptions.md", "## assumption_001\n")
    write(relate / "page-map.md", "## page_001\n")
    write(relate / "feature-map.md", "## feature_001\n")
    write(relate / "rule-map.md", "## rule_001\n")
    write(relate / "data-map.md", "## data_001\n")
    write(relate / "acceptance-map.md", "## acceptance_001\n")
    write(
        relate / "context-map.md",
        "fact_001 page_001 feature_001 rule_001 data_001 acceptance_001 question_001 conflict_001 assumption_001",
    )

    module = load_script("modules/relate/scripts/check-relate.py")
    result = module.check_relate(root)
    check_file = module.write_check(root, result)
    content = check_file.read_text()

    assert "## 1. 断链检查" in content
    assert "每个核心规则有关联数据对象" in content
    assert "本轮关联是否可以进入生成阶段" in content


def test_setup_installs_agent_configs_and_claude_commands(tmp_path: Path):
    module = load_script("scripts/setup-prd-helper.py")

    config_files = module.install_agent_configs(tmp_path, ["codex", "claude-code"])
    command_files = module.install_claude_commands(tmp_path, "docs/prd-helper")

    assert tmp_path / "AGENTS.md" in config_files
    assert tmp_path / "CLAUDE.md" in config_files
    assert "<!-- PRD-HELPER:START -->" in (tmp_path / "AGENTS.md").read_text()
    assert "<!-- PRD-HELPER:START -->" in (tmp_path / "CLAUDE.md").read_text()
    assert tmp_path / ".claude" / "commands" / "prd-start.md" in command_files
    assert not (tmp_path / ".claude" / "commands" / "prd-init.md").exists()
    assert not (tmp_path / ".claude" / "commands" / "prd-setup.md").exists()
    assert "collect-control.py\" start" in (tmp_path / ".claude" / "commands" / "prd-start.md").read_text()
