from pathlib import Path

from scripts.lib.install_state import (
    remove_project_commands,
    render_codex_project_config,
)


def test_render_codex_project_config_is_idempotent():
    content = "\n".join([
        'model = "gpt-5.5"',
        "",
        "[features]",
        "other_feature = false",
    ])

    first = render_codex_project_config(content, Path("/tmp/codex-marketplace"))
    second = render_codex_project_config(first, Path("/tmp/codex-marketplace"))

    assert first == second
    assert "[marketplaces.prd-helper-local]" in first
    assert '[plugins."prd-helper@prd-helper-local"]' in first
    assert "codex_hooks = true" in first
    assert "other_feature = false" in first


def test_remove_project_commands_removes_only_prd_commands(tmp_path: Path):
    commands = tmp_path / ".codex" / "commands"
    commands.mkdir(parents=True)
    (commands / "prd-start.md").write_text("start", encoding="utf-8")
    (commands / "prd-helper.md").write_text("helper", encoding="utf-8")
    (commands / "unrelated.md").write_text("keep", encoding="utf-8")

    removed = remove_project_commands(tmp_path, "codex")

    assert commands / "prd-start.md" in removed
    assert commands / "prd-helper.md" in removed
    assert not (commands / "prd-start.md").exists()
    assert (commands / "unrelated.md").exists()
