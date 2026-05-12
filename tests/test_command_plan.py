from pathlib import Path

from scripts.lib.command_plan import build_command_plan


def test_command_plan_runs_setup_before_start():
    plan = build_command_plan("start", Path("/runtime"), "docs/prd-helper", "codex")

    assert plan.requires_setup
    assert plan.command[1].endswith("modules/collect/scripts/collect-control.py")
    assert plan.command[2] == "start"
    assert "--agent" in plan.command
    assert "codex" in plan.command


def test_command_plan_remove_does_not_require_setup():
    plan = build_command_plan("remove", Path("/runtime"), "docs/prd-helper", "codex", ["--delete-docs"])

    assert not plan.requires_setup
    assert plan.command[1].endswith("scripts/remove-prd-helper.py")
    assert "--delete-docs" in plan.command


def test_command_plan_generate_uses_generate_runner():
    plan = build_command_plan("generate", Path("/runtime"), "docs/prd-helper", "claude-code")

    assert plan.requires_setup
    assert plan.command[1].endswith("modules/generate/scripts/generate.py")
    assert plan.command[-1] == "docs/prd-helper"
