from scripts.lib.command_packaging import dispatcher_lookup_snippet, render_command_markdown
from scripts.lib.command_registry import command_by_name


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
