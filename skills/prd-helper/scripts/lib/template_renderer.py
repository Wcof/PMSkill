"""Small UTF-8 Markdown template renderer."""

from __future__ import annotations

from pathlib import Path


def render_text_template(template: str, values: dict[str, object]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{" + key + "}", str(value))
    return rendered


def render_template(path: Path, values: dict[str, object]) -> str:
    return render_text_template(path.read_text(encoding="utf-8"), values)
