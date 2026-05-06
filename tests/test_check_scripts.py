import importlib.util
import json
import sys
from pathlib import Path

from scripts.lib.source_index import append_index, ensure_index
from scripts.lib.state import read_collect_state, write_collect_state


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
    write(root / "active" / "sessions" / "session-test.md", "---\nsource_id: turn-001\n---\n## Turn 1\n\n### User Query\n\nUser Query\n\n### Agent Answer\n\nAgent Answer\n")
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
            "path": "active/sessions/session-test.md",
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
    assert tmp_path / ".claude" / "commands" / "prd-helper.md" in command_files
    assert tmp_path / ".claude" / "commands" / "prd-start.md" in command_files
    assert not (tmp_path / ".claude" / "commands" / "prd-init.md").exists()
    assert not (tmp_path / ".claude" / "commands" / "prd-setup.md").exists()
    assert "setup-prd-helper.py" in (tmp_path / ".claude" / "commands" / "prd-helper.md").read_text()
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
    assert (tmp_path / ".claude" / "commands" / "prd-helper.md").exists()
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

    captured = list((root / "active" / "sessions").glob("session-*.md"))
    assert len(captured) == 1
    content = captured[0].read_text()
    assert "机器人巡检点位管理功能" in content
    assert "已记录这个需求" in content
    assert "active/sessions/" in (root / "source-index.md").read_text()


def test_scan_passive_indexes_new_files_and_updates_state(tmp_path: Path, monkeypatch):
    module = load_script("modules/collect/scripts/scan-passive.py")
    root = tmp_path / "docs" / "prd-helper" / "01-collect"
    passive = root / "passive"
    passive.mkdir(parents=True)
    write(
        passive / "meeting.md",
        """
- 来源：会议纪要
- 记录时间：2026-05-03
- 记录人：产品经理
- 责任人：业务负责人
- 优先级：高
""",
    )
    write_collect_state(root, {"capture_mode": "off", "passive_source_count": "0", "total_sources": "0"})

    monkeypatch.setattr(sys, "argv", ["scan-passive.py", "--root", str(root)])
    module.main()

    index = (root / "source-index.md").read_text()
    state = (root / "collect-state.md").read_text()
    assert "passive/meeting.md" in index
    assert "| passive_source_count | 1 |" in state
    assert "| total_sources | 1 |" in state


def test_remove_prd_helper_cleans_commands_and_hooks(tmp_path: Path):
    module = load_script("scripts/remove-prd-helper.py")
    commands = tmp_path / ".claude" / "commands"
    write(commands / "prd-helper.md", "helper")
    write(commands / "prd-start.md", "start")
    write(commands / "prd-stop.md", "stop")
    write(commands / "unrelated.md", "keep")
    write(
        tmp_path / ".claude" / "settings.json",
        """
{
  "hooks": {
    "UserPromptSubmit": [
      {"hooks": [{"type": "command", "command": "python3 \\"/old/claude-capture-hook.py\\""}]}
    ],
    "Stop": [
      {"hooks": [{"type": "command", "command": "python3 \\"/old/claude-capture-hook.py\\""}]}
    ]
  }
}
""".strip()
        + "\n",
    )

    module.remove_generated_commands(tmp_path, ["claude-code"])
    hook_file = module.remove_claude_hooks(tmp_path)

    assert not (commands / "prd-start.md").exists()
    assert not (commands / "prd-helper.md").exists()
    assert not (commands / "prd-stop.md").exists()
    assert (commands / "unrelated.md").exists()
    assert hook_file == tmp_path / ".claude" / "settings.json"
    assert "claude-capture-hook.py" not in (tmp_path / ".claude" / "settings.json").read_text()


def test_check_generated_template_paths_resolve_to_real_files():
    """check-generated.py 的模板路径必须指向实际存在的文件。"""
    module = load_script("modules/generate/scripts/check-generated.py")

    # page 模板路径应该存在
    page_template = (
        ROOT / "modules" / "generate" / "templates" / "04-generate-page-prd-template.md"
    )
    assert page_template.exists(), f"Page template missing: {page_template}"

    # rule 模板路径应该存在
    rule_template = (
        ROOT / "modules" / "generate" / "templates" / "04-generate-rule-prd-template.md"
    )
    assert rule_template.exists(), f"Rule template missing: {rule_template}"

    # check_page_completeness 内部使用的路径应该和实际路径一致
    # 当前 bug: Path(__file__).parent.parent / "modules" / "generate" / "templates" / ...
    # 实际解析为 modules/generate/modules/generate/templates/... (不存在)
    script_file = ROOT / "modules" / "generate" / "scripts" / "check-generated.py"
    buggy_path = script_file.parent.parent / "modules" / "generate" / "templates" / "04-generate-page-prd-template.md"
    assert not buggy_path.exists(), f"Bug path should NOT exist: {buggy_path}"

    # 正确路径
    correct_path = script_file.parent.parent / "templates" / "04-generate-page-prd-template.md"
    assert correct_path.exists(), f"Correct path should exist: {correct_path}"


def test_check_page_completeness_detects_missing_sections(tmp_path: Path):
    """check_page_completeness 应该能检测到页面缺少模板要求的章节。"""
    module = load_script("modules/generate/scripts/check-generated.py")

    # 创建一个缺少章节的页面文件
    pages_dir = tmp_path / "04-generate" / "pages"
    pages_dir.mkdir(parents=True)
    write(pages_dir / "test-page.md", "# Test Page\n\nSome content without required sections.\n")

    # 调用 check_page_completeness
    results = module.check_page_completeness(tmp_path)

    # 应该返回结果（不是空列表），并且状态为 FAIL
    assert len(results) > 0, "check_page_completeness returned empty — template path is broken"
    assert results[0]["status"] == "FAIL"
    assert len(results[0]["missing_sections"]) > 0


def test_claude_plugin_manifest_references_existing_commands():
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())

    assert plugin["name"] == "prd-helper"
    assert marketplace["plugins"][0]["source"] == "./"

    command_paths = plugin["commands"]
    assert "./commands/prd-helper.md" in command_paths
    assert "./commands/prd-start.md" in command_paths

    for command_path in command_paths:
        path = ROOT / command_path.removeprefix("./")
        assert path.exists(), command_path
        content = path.read_text()
        assert "allowed-tools: Bash" in content
        assert "find_prd_helper_root" in content


def test_bootstrap_file_does_not_exist():
    """bootstrap.py 应该被删除 — 所有脚本使用内联 one-liner。"""
    bootstrap_path = ROOT / "scripts" / "lib" / "bootstrap.py"
    assert not bootstrap_path.exists(), "bootstrap.py 应该被删除，所有脚本使用内联 sys.path 引导"


def test_module_scripts_do_not_contain_inline_bootstrap():
    """模块脚本不应包含内联的 sys.path 引导代码。"""
    bootstrap_pattern = "for _parent in Path(__file__).resolve().parents:"
    scripts = [
        "modules/collect/scripts/collect-control.py",
        "modules/collect/scripts/capture-source.py",
        "modules/collect/scripts/scan-all-sessions.py",
        "modules/collect/scripts/check-collect.py",
        "modules/collect/scripts/scan-passive.py",
        "modules/generate/scripts/check-generated.py",
        "modules/refine/scripts/check-refine.py",
        "modules/relate/scripts/check-relate.py",
    ]
    for script_path in scripts:
        content = (ROOT / script_path).read_text()
        assert bootstrap_pattern not in content, (
            f"{script_path} still contains inline bootstrap — use `from lib.bootstrap import *` instead"
        )


def test_default_state_contains_all_state_keys():
    """default_state() 应该为 STATE_KEYS 中的每个 key 提供默认值。"""
    from scripts.lib.state import STATE_KEYS, default_state
    state = default_state()
    for key in STATE_KEYS:
        assert key in state, f"default_state() missing key: {key}"


def test_write_collect_state_warns_on_unknown_keys(tmp_path: Path):
    """write_collect_state 应该对不在 STATE_KEYS 中的 key 发出警告。"""
    import warnings
    from scripts.lib.state import write_collect_state
    state = {"capture_mode": "on", "typo_key": "bad_value"}
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        write_collect_state(tmp_path, state)
        assert len(w) == 1
        assert "typo_key" in str(w[0].message)


def test_session_writer_creates_file_with_frontmatter(tmp_path: Path):
    """session_writer 应该创建包含标准 frontmatter 的会话文件。"""
    from scripts.lib.session_writer import create_session_file
    session_file = create_session_file(
        sessions_dir=tmp_path / "sessions",
        source_id="test-001",
        agent="claude-code",
        session_id="sess-001",
        turns=[("What is X?", "X is Y")],
    )
    assert session_file.exists()
    content = session_file.read_text()
    assert "source_id: test-001" in content
    assert "agent: claude-code" in content
    assert "## Turn 1" in content
    assert "### User Query" in content
    assert "What is X?" in content
    assert "### Agent Answer" in content
    assert "X is Y" in content


def test_session_writer_appends_turn_to_existing(tmp_path: Path):
    """session_writer 应该能向已有会话文件追加新轮次。"""
    from scripts.lib.session_writer import create_session_file, append_turn
    session_file = create_session_file(
        sessions_dir=tmp_path / "sessions",
        source_id="test-002",
        agent="claude-code",
        session_id="sess-002",
        turns=[("Q1", "A1")],
    )
    append_turn(session_file, turn_index=2, user_query="Q2", agent_answer="A2")
    content = session_file.read_text()
    assert "## Turn 1" in content
    assert "## Turn 2" in content
    assert "Q2" in content
    assert "A2" in content


def test_check_writer_produces_valid_check_md(tmp_path: Path):
    """CheckWriter 应该生成结构完整的 check.md。"""
    from scripts.lib.check_framework import CheckWriter
    output_dir = tmp_path / "02-refine"
    w = CheckWriter(output_dir, "精炼检查")
    w.add_meta("检查来源", "check-refine.py 自动生成")
    w.add_meta("检查状态", "通过")
    w.add_section("1. 文件检查", [
        (True, "facts.md 存在"),
        (False, "decisions.md 缺失"),
    ])
    w.add_conclusion(can_proceed=False, reason="decisions.md 缺失")
    check_file = w.write()

    assert check_file.exists()
    content = check_file.read_text()
    assert "# 精炼检查" in content
    assert "## 0. 检查信息" in content
    assert "检查来源" in content
    assert "## 1. 文件检查" in content
    assert "- [x] facts.md 存在" in content
    assert "- [ ] decisions.md 缺失" in content
    assert "## 结论" in content
    assert "- [x] 不可以" in content


def test_check_writer_custom_conclusion_heading_and_prompt(tmp_path: Path):
    """CheckWriter 应该支持自定义结论标题和提示文本。"""
    from scripts.lib.check_framework import CheckWriter
    w = CheckWriter(tmp_path, "关联检查")
    w.add_section("1. 断链检查", [(True, "fact→page")])
    w.add_conclusion(
        can_proceed=True,
        reason="自动检查通过",
        heading="4. 关联结论",
        prompt="本轮关联是否可以进入生成阶段：",
        proceed_label="可以",
    )
    content = w.write().read_text()
    assert "## 4. 关联结论" in content
    assert "本轮关联是否可以进入生成阶段：" in content
    assert "- [x] 可以" in content
    assert "- [ ] 不可以" in content


def test_valid_transitions_define_lifecycle():
    """VALID_TRANSITIONS 应该定义完整的采集生命周期。"""
    from scripts.lib.state import VALID_TRANSITIONS
    assert "off" in VALID_TRANSITIONS
    assert "on" in VALID_TRANSITIONS
    assert "paused" in VALID_TRANSITIONS
    # off -> on 是合法转换
    assert "on" in VALID_TRANSITIONS["off"]
    # on -> paused 是合法转换
    assert "paused" in VALID_TRANSITIONS["on"]
    # paused -> on 是合法转换
    assert "on" in VALID_TRANSITIONS["paused"]
    # on -> off 是合法转换
    assert "off" in VALID_TRANSITIONS["on"]
    # paused -> off 是合法转换
    assert "off" in VALID_TRANSITIONS["paused"]


def test_transition_rejects_invalid():
    """transition() 应该拒绝非法状态转换。"""
    from scripts.lib.state import transition, InvalidTransition
    # off -> paused 不合法
    try:
        transition("off", "paused")
        assert False, "Should have raised InvalidTransition"
    except InvalidTransition:
        pass
    # off -> off 不合法
    try:
        transition("off", "off")
        assert False, "Should have raised InvalidTransition"
    except InvalidTransition:
        pass


def test_transition_accepts_valid():
    """transition() 应该接受合法状态转换。"""
    from scripts.lib.state import transition
    assert transition("off", "on") == "on"
    assert transition("on", "paused") == "paused"
    assert transition("paused", "on") == "on"
    assert transition("on", "off") == "off"
    assert transition("paused", "off") == "off"


def test_cmd_start_reuses_existing_session(tmp_path: Path):
    """/prd-start 应该复用已有 session（capture_mode == 'off' 时）。"""
    module = load_script("modules/collect/scripts/collect-control.py")
    root = tmp_path / "01-collect"
    root.mkdir(parents=True, exist_ok=True)
    project = tmp_path

    # 写入已有状态：capture_mode 为 off，有 session_id
    write_collect_state(root, {
        "capture_mode": "off",
        "session_id": "prd-session-existing-123",
        "agent": "claude-code",
        "started_at": "2025-01-01T00:00:00Z",
        "ended_at": "2025-01-01T01:00:00Z",
        "total_sources": "5",
        "passive_source_count": "2",
    })

    # 调用 cmd_start
    module.cmd_start(root, "claude-code", project, str(tmp_path / "docs" / "prd-helper"))

    # 验证 session_id 被复用
    state = read_collect_state(root)
    assert state["session_id"] == "prd-session-existing-123", "应该复用已有 session_id"
    assert state["capture_mode"] == "on"


def test_cmd_start_uses_default_state(tmp_path: Path):
    """/prd-start 应该使用 default_state() 构造基础状态。"""
    from scripts.lib.state import STATE_KEYS
    module = load_script("modules/collect/scripts/collect-control.py")
    root = tmp_path / "01-collect"
    root.mkdir(parents=True, exist_ok=True)

    module.cmd_start(root, "claude-code", tmp_path, "docs/prd-helper")

    state = read_collect_state(root)
    # 所有 STATE_KEYS 都应该存在
    for key in STATE_KEYS:
        assert key in state, f"cmd_start 缺少 STATE_KEY: {key}"
    # 特定字段应该被正确覆盖
    assert state["capture_mode"] == "on"
    assert state["agent"] == "claude-code"
    assert state["session_id"].startswith("prd-session-")
    assert state["started_at"] != ""
    assert state["grill_mode"] == "off"


def test_cmd_start_source_uses_default_state_function():
    """/prd-start 源码应该引用 default_state() 而非手动构造字典。"""
    source = (ROOT / "modules" / "collect" / "scripts" / "collect-control.py").read_text()
    assert "default_state()" in source, "cmd_start 应该使用 default_state() 构造基础状态"
    # 确认不再有手动构造空值 key 的代码（这些应由 default_state() 提供）
    assert '"paused_at":' not in source, "不应手动构造 paused_at，应由 default_state() 提供"
    assert '"last_collect_at":' not in source, "不应手动构造 last_collect_at，应由 default_state() 提供"
    assert '"last_source_id":' not in source, "不应手动构造 last_source_id，应由 default_state() 提供"
    assert '"last_content_hash":' not in source, "不应手动构造 last_content_hash，应由 default_state() 提供"
    assert '"last_write_file":' not in source, "不应手动构造 last_write_file，应由 default_state() 提供"
    assert '"anomaly_count":' not in source, "不应手动构造 anomaly_count，应由 default_state() 提供"
    assert '"possible_noise_count":' not in source, "不应手动构造 possible_noise_count，应由 default_state() 提供"


def test_cmd_stop_outputs_refine_hint(tmp_path: Path, capsys):
    """/prd-stop 应该输出精炼提示。"""
    module = load_script("modules/collect/scripts/collect-control.py")
    root = tmp_path / "01-collect"
    root.mkdir(parents=True, exist_ok=True)
    project = tmp_path

    # 写入已有状态：capture_mode 为 on
    write_collect_state(root, {
        "capture_mode": "on",
        "session_id": "prd-session-test-456",
        "agent": "claude-code",
        "started_at": "2025-01-01T00:00:00Z",
    })

    # 调用 cmd_stop
    module.cmd_stop(root, "claude-code", project)

    # 验证输出包含精炼提示
    captured = capsys.readouterr()
    assert "/prd-refine" in captured.out, "应该提示可以用 /prd-refine"


def test_discovery_write_session_uses_session_writer(tmp_path: Path):
    """discovery.write_session 应该使用 session_writer 而非自行构建内容。"""
    from scripts.lib.discovery import write_session, Session

    collect_root = tmp_path / "01-collect"
    (collect_root / "active" / "sessions").mkdir(parents=True)

    session = Session(
        id="test-session-001",
        turns=[("What is X?", "X is Y", "2026-01-01T00:00:00Z")],
    )
    write_session("claude", session, collect_root, set())

    sessions_dir = collect_root / "active" / "sessions"
    files = list(sessions_dir.glob("session-*.md"))
    assert len(files) == 1
    content = files[0].read_text()
    # 应该包含标准 frontmatter 字段
    assert "source_id:" in content
    assert "agent: claude" in content
    assert "## Turn 1" in content
    assert "### User Query" in content
    assert "What is X?" in content


def test_discovery_does_not_contain_build_session_content():
    """discovery.py 不应包含 build_session_content 函数。"""
    source = (ROOT / "scripts" / "lib" / "discovery.py").read_text()
    assert "def build_session_content" not in source, (
        "build_session_content 应该被删除，改用 session_writer.create_session_file"
    )


def test_collect_control_uses_transition(tmp_path: Path):
    """collect-control.py 应该使用 transition() 验证状态转换。"""
    source = (ROOT / "modules" / "collect" / "scripts" / "collect-control.py").read_text()
    assert "transition(" in source, "collect-control.py 应该调用 transition() 验证状态转换"
    assert "InvalidTransition" in source, "collect-control.py 应该捕获 InvalidTransition 异常"


def test_cmd_stop_rejects_invalid_transition(tmp_path: Path, capsys):
    """/prd-stop 在 capture_mode=off 时应该拒绝并提示。"""
    module = load_script("modules/collect/scripts/collect-control.py")
    root = tmp_path / "01-collect"
    root.mkdir(parents=True, exist_ok=True)

    write_collect_state(root, {"capture_mode": "off", "session_id": ""})
    module.cmd_stop(root, "claude-code", tmp_path)

    captured = capsys.readouterr()
    assert "Cannot stop" in captured.out or "非法" in captured.out or "InvalidTransition" in captured.out
