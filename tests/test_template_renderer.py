from pathlib import Path

from scripts.lib.template_renderer import render_text_template, render_template


def test_render_text_template_basic():
    template = "Hello {name}, welcome to {project}!"
    result = render_text_template(template, {"name": "Alice", "project": "PRD"})
    assert result == "Hello Alice, welcome to PRD!"


def test_render_text_template_no_placeholders():
    assert render_text_template("no placeholders", {"key": "val"}) == "no placeholders"


def test_render_text_template_missing_key():
    # Keys not in values are left as-is
    result = render_text_template("{a} and {b}", {"a": "X"})
    assert result == "X and {b}"


def test_render_text_template_empty_values():
    assert render_text_template("{x}", {}) == "{x}"


def test_render_text_template_numeric_value():
    result = render_text_template("count: {n}", {"n": 42})
    assert result == "count: 42"


def test_render_template_from_file(tmp_path: Path):
    t = tmp_path / "t.md"
    t.write_text("# {title}\n\nStatus: {status}\n", encoding="utf-8")
    result = render_template(t, {"title": "My PRD", "status": "draft"})
    assert result == "# My PRD\n\nStatus: draft\n"
