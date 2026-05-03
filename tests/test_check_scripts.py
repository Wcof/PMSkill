import importlib.util
import json
import sys
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
    assert "--project . --docs-root docs/prd-helper --agent claude-code" in (
        tmp_path / ".claude" / "commands" / "prd-start.md"
    ).read_text()
    assert not (tmp_path / ".claude" / "settings.json").exists()


def test_setup_main_repairs_partial_claude_initialization(tmp_path: Path, monkeypatch):
    module = load_script("scripts/setup-prd-helper.py")
    docs_root = tmp_path / "docs" / "prd-helper"
    write(docs_root / "prd-helper-config.md", "# existing config\n")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "setup-prd-helper.py",
            "--project",
            str(tmp_path),
            "--docs-root",
            "docs/prd-helper",
            "--agent",
            "claude-code",
        ],
    )

    assert module.main() == 0
    assert (docs_root / "prd-helper-config.md").read_text() == "# existing config\n"
    assert (tmp_path / ".claude" / "commands" / "prd-start.md").exists()
    assert (tmp_path / ".claude" / "commands" / "prd-status.md").exists()
    assert not (tmp_path / ".claude" / "settings.json").exists()
    assert not (tmp_path / ".claude" / "commands" / "prd-init.md").exists()


def test_collect_control_toggles_claude_hooks(tmp_path: Path):
    module = load_script("modules/collect/scripts/collect-control.py")
    root = tmp_path / "docs" / "prd-helper" / "01-collect"

    module.cmd_start(root, "claude-code", tmp_path, "docs/prd-helper")
    settings_file = tmp_path / ".claude" / "settings.json"
    settings = json.loads(settings_file.read_text())
    assert "claude-capture-hook.py" in settings["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
    assert "claude-capture-hook.py" in settings["hooks"]["Stop"][0]["hooks"][0]["command"]

    module.cmd_pause(root, "claude-code", tmp_path)
    assert "claude-capture-hook.py" not in settings_file.read_text()

    module.cmd_resume(root, "claude-code", tmp_path, "docs/prd-helper")
    assert "claude-capture-hook.py" in settings_file.read_text()

    module.cmd_stop(root, "claude-code", tmp_path)
    assert "claude-capture-hook.py" not in settings_file.read_text()


def test_collect_start_repairs_hooks_when_already_capturing(tmp_path: Path):
    module = load_script("modules/collect/scripts/collect-control.py")
    root = tmp_path / "docs" / "prd-helper" / "01-collect"

    module.cmd_start(root, "claude-code", tmp_path, "docs/prd-helper")
    settings_file = tmp_path / ".claude" / "settings.json"
    settings_file.write_text(
        """
{
  "hooks": {
    "UserPromptSubmit": [
      {"hooks": [{"type": "command", "command": "python3 \\"/old/path/claude-capture-hook.py\\""}]}
    ],
    "Stop": [
      {"hooks": [{"type": "command", "command": "python3 \\"/old/path/claude-capture-hook.py\\""}]}
    ]
  }
}
""".strip()
        + "\n"
    )

    module.cmd_start(root, "claude-code", tmp_path, "docs/prd-helper")
    settings = settings_file.read_text()
    assert "/old/path/claude-capture-hook.py" not in settings
    assert settings.count("claude-capture-hook.py") == 2


def test_claude_capture_hook_records_turn_after_start(tmp_path: Path):
    module = load_script("scripts/claude-capture-hook.py")
    root = tmp_path / "docs" / "prd-helper" / "01-collect"
    root.mkdir(parents=True)
    write_collect_state(
        root,
        {
            "capture_mode": "on",
            "session_id": "prd-session-test",
            "turn_count": "0",
            "active_source_count": "0",
            "total_sources": "0",
            "possible_noise_count": "0",
        },
    )

    prompt_payload = {
        "session_id": "session-001",
        "cwd": str(tmp_path),
        "hook_event_name": "UserPromptSubmit",
        "prompt": "我们需要一个机器人巡检点位管理功能。",
    }
    stop_payload = {
        "session_id": "session-001",
        "cwd": str(tmp_path),
        "hook_event_name": "Stop",
        "last_assistant_message": "已记录这个需求，并会保留原始上下文。",
    }

    assert module.handle_user_prompt(prompt_payload, root, tmp_path) == 0
    assert module.handle_stop(stop_payload, root, tmp_path, "claude-code") == 0

    captured = list((root / "active" / "sessions").glob("turn-*.md"))
    assert len(captured) == 1
    content = captured[0].read_text()
    assert "机器人巡检点位管理功能" in content
    assert "已记录这个需求" in content
    assert "active/sessions/" in (root / "source-index.md").read_text()
