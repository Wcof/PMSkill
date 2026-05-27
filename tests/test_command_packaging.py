from pathlib import Path

from scripts.lib.command_packaging import dispatcher_lookup_snippet, render_command_markdown
from scripts.lib.command_registry import ALL_COMMANDS, command_by_name

ROOT = Path(__file__).resolve().parents[1]


def test_command_packaging_renders_canonical_command_markdown():
    command = command_by_name("prd-start")
    content = render_command_markdown(command, include_skill_frontmatter=False)

    assert command.zh_description in content
    assert dispatcher_lookup_snippet("prd-start") in content
    assert "python3 \"$dispatcher\" start --project . --docs-root docs/prd-helper" in content


def test_command_packaging_renders_skill_markdown_with_name():
    command = command_by_name("prd-start")
    content = render_command_markdown(command, include_skill_frontmatter=True)

    assert "name: prd-start" in content
    assert dispatcher_lookup_snippet("prd-start") in content


def test_command_files_contain_matching_dispatcher_snippet():
    """每个 commands/*.md 文件应包含对应命令的 dispatcher snippet。"""
    for command in ALL_COMMANDS:
        content = (ROOT / "commands" / f"{command.name}.md").read_text(encoding="utf-8")
        snippet = dispatcher_lookup_snippet(command.name)
        assert snippet in content, f"commands/{command.name}.md missing canonical dispatcher snippet"


def test_skill_files_contain_matching_dispatcher_snippet():
    """每个 skills/*/SKILL.md 文件应包含对应命令的 dispatcher snippet。"""
    for command in ALL_COMMANDS:
        if command.name == "prd-helper":
            continue  # prd-helper has its own SKILL.md format
        content = (ROOT / "skills" / command.name / "SKILL.md").read_text(encoding="utf-8")
        snippet = dispatcher_lookup_snippet(command.name)
        assert snippet in content, f"skills/{command.name}/SKILL.md missing canonical dispatcher snippet"


def test_command_files_match_generated_content():
    """commands/*.md 文件应与 render_command_markdown() 生成的内容完全一致。"""
    for command in ALL_COMMANDS:
        expected = render_command_markdown(command, include_skill_frontmatter=False)
        actual = (ROOT / "commands" / f"{command.name}.md").read_text(encoding="utf-8")
        assert actual == expected, f"commands/{command.name}.md differs from generated content — regenerate with command_packaging"


def test_codex_plugin_command_files_match_generated_content():
    """codex plugin 的 commands/*.md 也应与生成内容一致。"""
    for command in ALL_COMMANDS:
        expected = render_command_markdown(command, include_skill_frontmatter=False)
        path = ROOT / "support" / "adapters" / "codex" / "plugin" / "commands" / f"{command.name}.md"
        actual = path.read_text(encoding="utf-8")
        assert actual == expected, f"{path.relative_to(ROOT)} differs from generated content"
