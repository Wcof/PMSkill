#!/usr/bin/env python3
"""通过 Agent 指令从当前项目卸载 PRD Helper。"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.claude_hooks import remove_claude_hooks
from lib.codex_hooks import remove_codex_hooks
from lib.constants import (
    CODEX_TMP_MARKETPLACES_REL,
    CODEX_TMP_PLUGIN_CACHE_REL,
    CODEX_TMP_PLUGIN_SHA_REL,
    CODEX_TMP_REMOTE_SYNC_REL,
    COMMAND_NAMES,
)


AGENTS = ("codex", "claude-code", "trae", "trae-cn")
LEGACY_CLAUDE_COMMANDS = ("prd-helper.md", "prd-init.md", "prd-setup.md")
CLAUDE_COMMANDS = tuple(f"{name}.md" for name in COMMAND_NAMES) + LEGACY_CLAUDE_COMMANDS


def invalidate_codex_plugin_cache(codex_home: Path) -> list[Path]:
    removed: list[Path] = []
    for relative in (
        CODEX_TMP_PLUGIN_CACHE_REL,
        CODEX_TMP_MARKETPLACES_REL,
        CODEX_TMP_REMOTE_SYNC_REL,
    ):
        target = codex_home / relative
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            removed.append(target)

    sha_file = codex_home / CODEX_TMP_PLUGIN_SHA_REL
    if sha_file.exists():
        sha_file.unlink()
        removed.append(sha_file)
    return removed


def remove_codex_plugin() -> None:
    """Remove PRD Helper Codex plugin from ~/.codex/plugins/prd-helper/."""
    from lib.discovery import find_codex_home
    from lib.constants import CODEX_LOCAL_MARKETPLACE_REL, CODEX_PLUGIN_DIR

    codex_home = find_codex_home()
    plugin_dir = codex_home / CODEX_PLUGIN_DIR
    marketplace_dir = codex_home / CODEX_LOCAL_MARKETPLACE_REL

    if plugin_dir.exists():
        shutil.rmtree(plugin_dir)
        print(f"已删除 Codex 插件：{plugin_dir}")
    else:
        print("Codex 插件目录不存在，跳过清理。")
    if marketplace_dir.exists():
        shutil.rmtree(marketplace_dir)
        print(f"已删除 Codex marketplace：{marketplace_dir}")
    for path in invalidate_codex_plugin_cache(codex_home):
        print(f"已失效 Codex 插件缓存：{path}")


def _remove_toml_tables(content: str, table_headers: set[str]) -> str:
    lines = content.splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].strip() in table_headers:
            index += 1
            while index < len(lines) and not lines[index].startswith("["):
                index += 1
            if output and output[-1] == "":
                output.pop()
            continue
        output.append(lines[index])
        index += 1
    return "\n".join(output).rstrip() + ("\n" if output else "")


def _remove_toml_key_from_table(content: str, table_header: str, key_prefix: str) -> str:
    lines = content.splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.strip() != table_header:
            output.append(line)
            index += 1
            continue

        body: list[str] = []
        index += 1
        while index < len(lines) and not lines[index].startswith("["):
            if not lines[index].strip().startswith(key_prefix):
                body.append(lines[index])
            index += 1

        non_empty_body = [entry for entry in body if entry.strip()]
        if non_empty_body:
            if output and output[-1] != "":
                output.append("")
            output.append(table_header)
            output.extend(body)
        elif output and output[-1] == "":
            output.pop()

    return "\n".join(output).rstrip() + ("\n" if output else "")


def remove_codex_config_entries(config_path: Path) -> None:
    if not config_path.exists():
        return
    from lib.constants import CODEX_LOCAL_MARKETPLACE_NAME, CODEX_LOCAL_PLUGIN_REF

    content = config_path.read_text(encoding="utf-8")
    updated = _remove_toml_tables(
        content,
        {
            f"[marketplaces.{CODEX_LOCAL_MARKETPLACE_NAME}]",
            f'[plugins."{CODEX_LOCAL_PLUGIN_REF}"]',
        },
    )
    updated = _remove_toml_key_from_table(updated, "[features]", "codex_hooks")
    if updated.strip():
        config_path.write_text(updated, encoding="utf-8")
    else:
        config_path.unlink()
    print(f"已清理 Codex 配置：{config_path}")


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def run(cmd: list[str], cwd: Path) -> int:
    print("+ " + " ".join(cmd))
    completed = subprocess.run(cmd, cwd=str(cwd), check=False)
    return completed.returncode


def remove_generated_commands(project: Path, agents: list[str]) -> None:
    if "claude-code" in agents:
        commands_dir = project / ".claude" / "commands"
        for name in CLAUDE_COMMANDS:
            path = commands_dir / name
            if path.exists():
                path.unlink()
                print(f"已删除 Claude Code 命令：{path}")
    if "codex" in agents:
        commands_dir = project / ".codex" / "commands"
        for name in CLAUDE_COMMANDS:
            path = commands_dir / name
            if path.exists():
                path.unlink()
                print(f"已删除 Codex 命令：{path}")


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

    if "codex" in agents:
        hook_file = remove_codex_hooks(project)
        if hook_file:
            print(f"已清理 Codex Hook 配置：{hook_file}")
        remove_codex_plugin()
        from lib.discovery import find_codex_home

        remove_codex_config_entries(find_codex_home() / "config.toml")
        remove_codex_config_entries(project / ".codex" / "config.toml")

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
