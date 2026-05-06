from pathlib import Path

from scripts.lib.command_registry import ALL_COMMANDS, GENERATED_COMMAND_NAMES
from scripts.lib.constants import COMMAND_NAMES


ROOT = Path(__file__).resolve().parents[1]
CURRENT_COMMANDS = {"/prd-helper", *(f"/{name}" for name in COMMAND_NAMES)}
LEGACY_COMMANDS = {"/prd-pause", "/prd-resume", "/prd-grill"}


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_public_command_docs_use_current_command_set():
    docs = {
        "README.md": _read("README.md"),
        "README.en.md": _read("README.en.md"),
        "SKILL.md": _read("SKILL.md"),
        "docs/adr/0003-atomic-commands.md": _read("docs/adr/0003-atomic-commands.md"),
        "support/adapters/canonical-rules.md": _read("support/adapters/canonical-rules.md"),
    }

    for path, content in docs.items():
        for command in CURRENT_COMMANDS:
            assert command in content, f"{path} missing {command}"
        for command in LEGACY_COMMANDS:
            assert command not in content, f"{path} still mentions legacy {command}"


def test_constants_are_derived_from_command_registry():
    assert COMMAND_NAMES == GENERATED_COMMAND_NAMES
    assert {command.name for command in ALL_COMMANDS} == {command.removeprefix("/") for command in CURRENT_COMMANDS}


def test_command_files_match_constants():
    command_files = {
        f"/{path.stem}"
        for path in (ROOT / "commands").glob("prd-*.md")
    }
    assert command_files == CURRENT_COMMANDS

    for command in ALL_COMMANDS:
        content = _read(f"commands/{command.name}.md")
        assert command.slash in content
        assert command.zh_description in content


def test_codex_plugin_command_templates_match_current_command_set():
    command_files = {
        f"/{path.stem}"
        for path in (ROOT / "support/adapters/codex/plugin/commands").glob("prd-*.md")
    }
    assert command_files == CURRENT_COMMANDS


def test_setup_uses_static_templates_and_command_registry():
    setup = _read("scripts/setup-prd-helper.py")
    assert "_COLLECT_DESCRIPTIONS" not in setup
    assert "CLAUDE_COMMANDS" not in setup
    assert "prd-helper-config-template.md" in setup
    assert "collect-readme-template.md" in setup
    assert "command_markdown_list" in setup

    config_template = _read("modules/collect/templates/prd-helper-config-template.md")
    assert "{docs_root}" in config_template
    assert "{command_list}" in config_template


def test_check_scripts_are_template_driven():
    scripts = {
        "modules/collect/scripts/check-collect.py": "01-collect-check-template.md",
        "modules/refine/scripts/check-refine.py": "02-refine-check-template.md",
        "modules/relate/scripts/check-relate.py": "03-relate-check-template.md",
        "modules/generate/scripts/check-generated.py": "04-generate-check-template.md",
    }
    for path, template in scripts.items():
        content = _read(path)
        assert template in content
        assert "add_template_section" in content


def test_guides_keep_four_stage_model_and_discuss_auxiliary():
    skill = _read("SKILL.md")
    context = _read("CONTEXT.md")
    discuss = _read("modules/grill/guide.md")

    for content in (skill, context):
        for phase in ("Collect", "Refine", "Relate", "Generate"):
            assert phase in content
        assert "检查（Check）" in content
        assert "不是第五" in content

    assert "辅助能力" in discuss
    assert "不是第五" in discuss
    assert "/prd-discuss" in discuss
    for command in LEGACY_COMMANDS:
        assert command not in discuss
    assert "battle" not in discuss.lower()


def test_module_guides_state_stage_boundaries():
    collect = _read("modules/collect/guide.md")
    refine = _read("modules/refine/guide.md")
    relate = _read("modules/relate/guide.md")
    generate = _read("modules/generate/guide.md")

    assert "不做事实提取" in collect
    assert "/prd-import" in collect
    for command in LEGACY_COMMANDS:
        assert command not in collect

    assert "产物边界" in refine
    assert "如果一条信息既像事实又像推断" in refine
    assert "不代表关系完整" in refine

    assert "最小完整链路" in relate
    assert "fact -> page/feature -> rule -> data" in relate
    assert "RELATION_CHAIN_RULES" in relate

    assert "不得新增未来源化、未关联的业务规则" in generate
    assert "Agent 上下文边界" in generate
    assert "product-review-context.md" in generate
