#!/usr/bin/env python3
"""通过 Agent 指令从当前项目卸载 PRD Helper。"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.claude_hooks import remove_claude_hooks
from lib.constants import COMMAND_NAMES


AGENTS = ("codex", "claude-code", "trae", "trae-cn")
LEGACY_CLAUDE_COMMANDS = ("prd-init.md", "prd-setup.md")
CLAUDE_COMMANDS = tuple(f"{name}.md" for name in COMMAND_NAMES) + LEGACY_CLAUDE_COMMANDS


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def run(cmd: list[str], cwd: Path) -> int:
    print("+ " + " ".join(cmd))
    completed = subprocess.run(cmd, cwd=str(cwd), check=False)
    return completed.returncode


def remove_generated_commands(project: Path, agents: list[str]) -> None:
    if "claude-code" not in agents:
        return
    commands_dir = project / ".claude" / "commands"
    for name in CLAUDE_COMMANDS:
        path = commands_dir / name
        if path.exists():
            path.unlink()
            print(f"已删除 Claude Code 命令：{path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="卸载 PRD Helper（Remove PRD Helper）", add_help=False)
    parser._optionals.title = "可选参数（optional arguments）"
    parser.add_argument("-h", "--help", action="help", help="显示帮助信息并退出（show help and exit）。")
    parser.add_argument("--project", default=".", help="目标项目根目录（project root），默认当前目录。")
    parser.add_argument(
        "--agent",
        action="append",
        choices=AGENTS,
        help="要卸载的 Agent，可重复传入；默认所有支持的 Agent。",
    )
    parser.add_argument("--global", dest="global_scope", action="store_true", help="卸载全局安装（global install）。")
    parser.add_argument("--keep-docs", action="store_true", help="保留 docs/prd-helper 产物，默认行为。")
    parser.add_argument("--delete-docs", action="store_true", help="同时删除 docs/prd-helper 产物。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = Path(args.project).resolve()
    agents = args.agent or list(AGENTS)

    clean_cmd = [
        sys.executable,
        str(script_dir() / "clean-agent-config.py"),
        "--project",
        str(project),
    ]
    for agent in agents:
        clean_cmd.extend(["--agent", agent])

    clean_code = run(clean_cmd, project)
    if clean_code != 0:
        return clean_code
    remove_generated_commands(project, agents)
    if "claude-code" in agents:
        hook_file = remove_claude_hooks(project)
        if hook_file:
            print(f"已清理 Claude Code Hook 配置：{hook_file}")

    remove_cmd = [
        "npx",
        "skills@latest",
        "remove",
        "prd-helper",
        "--agent",
        *agents,
        "-y",
    ]
    if args.global_scope:
        remove_cmd.append("--global")

    remove_code = run(remove_cmd, project)
    if remove_code != 0:
        return remove_code

    if args.delete_docs:
        docs = project / "docs" / "prd-helper"
        if docs.exists():
            import shutil

            shutil.rmtree(docs)
            print(f"已删除（Deleted）：{docs}")
    elif not args.keep_docs:
        print("已保留生成文档：docs/prd-helper/。如需删除，请使用 --delete-docs。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
