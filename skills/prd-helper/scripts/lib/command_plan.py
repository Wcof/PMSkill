"""Execution plans for PRD Helper Atomic Commands."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass(frozen=True)
class CommandPlan:
    command: list[str]
    requires_setup: bool = True
    message: str = ""


def build_setup_command(skill_root: Path, docs_root: str, agent: str) -> list[str]:
    return [
        sys.executable,
        str(skill_root / "scripts" / "setup-prd-helper.py"),
        "--project",
        ".",
        "--docs-root",
        docs_root,
        "--agent",
        agent,
    ]


def build_command_plan(
    command: str,
    skill_root: Path,
    docs_root: str,
    agent: str,
    extra: list[str] | None = None,
) -> CommandPlan:
    extra = extra or []
    if command == "remove":
        return CommandPlan(
            [
                sys.executable,
                str(skill_root / "scripts" / "remove-prd-helper.py"),
                "--project",
                ".",
                "--agent",
                agent,
                *extra,
            ],
            requires_setup=False,
        )

    if command == "helper":
        return CommandPlan([], requires_setup=True)

    collect_root = f"{docs_root}/01-collect"
    if command in {"start", "stop", "status", "scan"}:
        return CommandPlan(
            [
                sys.executable,
                str(skill_root / "modules" / "collect" / "scripts" / "collect-control.py"),
                command,
                "--root",
                collect_root,
                "--project",
                ".",
                "--docs-root",
                docs_root,
                "--agent",
                agent,
            ]
        )
    if command == "refine":
        return CommandPlan([sys.executable, str(skill_root / "modules" / "refine" / "scripts" / "check-refine.py"), docs_root])
    if command == "relate":
        return CommandPlan([sys.executable, str(skill_root / "modules" / "relate" / "scripts" / "check-relate.py"), docs_root])
    if command == "generate":
        return CommandPlan([sys.executable, str(skill_root / "modules" / "generate" / "scripts" / "generate.py"), docs_root])
    if command in {"import", "discuss"}:
        return CommandPlan(
            [],
            requires_setup=True,
            message=f"/prd-{command} 已完成初始化。请按该命令 Skill 的说明继续处理用户输入。",
        )
    raise ValueError(f"Unknown PRD command: {command}")
