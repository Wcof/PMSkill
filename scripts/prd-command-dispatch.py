#!/usr/bin/env python3
"""Dispatch installed /prd-* skills to the PRD Helper runtime scripts."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.command_plan import build_command_plan, build_setup_command


COMMANDS = (
    "helper",
    "start",
    "stop",
    "status",
    "scan",
    "import",
    "refine",
    "relate",
    "generate",
    "discuss",
    "remove",
)


def _has_runtime(path: Path) -> bool:
    return (path / "scripts" / "setup-prd-helper.py").exists()


def _home(env: dict[str, str], name: str, fallback: str) -> Path:
    return Path(env.get(name, fallback)).expanduser()


def _runtime_from_dispatcher_path() -> Path | None:
    """Resolve runtime root when this script is executed from an installed skill."""
    current = Path(__file__).resolve()
    # installed path: .../<skill-name>/scripts/prd-command-dispatch.py
    skill_root = current.parent.parent
    if _has_runtime(skill_root):
        return skill_root
    return None


def candidate_roots(project: Path, env: dict[str, str]) -> list[Path]:
    codex_home = _home(env, "CODEX_HOME", "~/.codex")
    claude_home = _home(env, "CLAUDE_CONFIG_DIR", "~/.claude")
    roots: list[Path] = []

    # Prefer project-local helper runtime before global/plugin fallbacks.
    for base in (project / ".agents" / "skills", project / ".claude" / "skills", project / ".trae" / "skills"):
        roots.append(base / "prd-helper")

    # Local repo runtime.
    roots.append(project)

    runtime_from_script = _runtime_from_dispatcher_path()
    if runtime_from_script:
        roots.append(runtime_from_script)

    # Codex plugin runtimes written by setup script.
    roots.extend(
        [
            codex_home / "plugins" / "prd-helper" / "skills" / "prd-helper",
            codex_home / "local-marketplaces" / "prd-helper" / "plugins" / "prd-helper" / "skills" / "prd-helper",
        ]
    )

    # Claude cache fallback, but only explicit prd-helper setup scripts.
    cache = claude_home / "plugins" / "cache"
    if cache.exists():
        roots.extend(path.parent.parent for path in cache.glob("**/prd-helper/**/scripts/setup-prd-helper.py"))

    # Keep order but remove duplicates.
    unique: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        if root not in seen:
            seen.add(root)
            unique.append(root)
    return unique


def find_skill_root(project: Path, env: dict[str, str] | None = None) -> Path:
    env = env or os.environ
    for root in candidate_roots(project, env):
        if _has_runtime(root):
            return root
    raise FileNotFoundError("未找到 PRD Helper 运行时。请先运行 npx skills@latest add Wcof/PRDContextEngine")


def detect_agent(project: Path, env: dict[str, str] | None = None, skill_root: Path | None = None) -> str:
    env = env or os.environ
    if skill_root:
        parts = set(skill_root.parts)
        if ".claude" in parts:
            return "claude-code"
        if ".trae" in parts:
            return "trae"
        if ".codex" in parts:
            return "codex"
    if (project / ".codex").exists() or env.get("CODEX_HOME"):
        return "codex"
    if (project / ".claude").exists() or env.get("CLAUDE_CONFIG_DIR"):
        return "claude-code"
    if (project / ".trae").exists() or (project / "project_rules.md").exists():
        return "trae"
    return "claude-code"


def _run(cmd: list[str], project: Path) -> int:
    return subprocess.run(cmd, cwd=str(project), check=False).returncode


def _setup(skill_root: Path, project: Path, docs_root: str, agent: str) -> int:
    return _run(build_setup_command(skill_root, docs_root, agent), project)


def _dispatch(command: str, skill_root: Path, project: Path, docs_root: str, agent: str, extra: list[str]) -> int:
    plan = build_command_plan(command, skill_root, docs_root, agent, extra)
    if not plan.requires_setup:
        return _run(plan.command, project)

    setup_code = _setup(skill_root, project, docs_root, agent)
    if setup_code != 0:
        return setup_code

    if not plan.command:
        if plan.message:
            print(plan.message)
        return 0
    return _run(plan.command, project)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dispatch PRD Helper slash commands")
    parser.add_argument("command", choices=COMMANDS)
    parser.add_argument("--project", default=".")
    parser.add_argument("--docs-root", default="docs/prd-helper")
    parser.add_argument("--agent", choices=("codex", "claude-code", "trae", "trae-cn"))
    parser.add_argument("--diagnose", action="store_true", help="输出运行时选择诊断信息")
    parser.add_argument("extra", nargs=argparse.REMAINDER)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = Path(args.project).resolve()
    skill_root = find_skill_root(project, os.environ)
    agent = args.agent or detect_agent(project, os.environ, skill_root)
    if args.diagnose:
        print(f"[prd-dispatch] project={project}", file=sys.stderr)
        print(f"[prd-dispatch] skill_root={skill_root}", file=sys.stderr)
        print(f"[prd-dispatch] agent={agent}", file=sys.stderr)
    return _dispatch(args.command, skill_root, project, args.docs_root, agent, args.extra)


if __name__ == "__main__":
    raise SystemExit(main())
