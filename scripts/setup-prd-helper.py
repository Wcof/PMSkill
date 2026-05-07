#!/usr/bin/env python3
"""通过 Agent 指令初始化 PRD Helper 项目配置。"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.command_registry import ALL_COMMANDS, GENERATED_COMMANDS, command_markdown_list
from lib.source_index import INDEX_HEADER
from lib.state import write_collect_state
AGENTS = ("codex", "claude-code", "trae", "trae-cn")
PRD_BLOCK_START = "<!-- PRD-HELPER:START -->"
PRD_BLOCK_END = "<!-- PRD-HELPER:END -->"
ADAPTER_FILES = {
    "codex": ("AGENTS.md", "support/adapters/codex/AGENTS.md"),
    "claude-code": ("CLAUDE.md", "support/adapters/claude-code/CLAUDE.md"),
    "trae": ("project_rules.md", "support/adapters/trae/project_rules.md"),
    "trae-cn": ("project_rules.md", "support/adapters/trae/project_rules.md"),
}

# /prd-helper 同时写成项目级命令，作为 Claude Code skill 入口补全不刷新时的兜底。
_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPT_DIR.parent
_COLLECT_CONTROL = _SKILL_ROOT / "modules" / "collect" / "scripts" / "collect-control.py"
_REMOVE_SCRIPT = _SCRIPT_DIR / "remove-prd-helper.py"

MODULE_DIRS = (
    "01-collect/active/sessions",
    "01-collect/passive",
    "01-collect/grill",
    "02-refine",
    "03-relate",
    "04-generate/overview",
    "04-generate/pages",
    "04-generate/rules",
    "04-generate/data",
    "04-generate/acceptance",
    "04-generate/agent-context",
    "05-check",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="初始化 PRD Helper（Set up PRD Helper）", add_help=False)
    parser._optionals.title = "可选参数（optional arguments）"
    parser.add_argument("-h", "--help", action="help", help="显示帮助信息并退出（show help and exit）。")
    parser.add_argument("--project", default=".", help="目标项目根目录（project root），默认当前目录。")
    parser.add_argument("--docs-root", default="docs/prd-helper", help="PRD Helper 文档保存目录（docs root）。")
    parser.add_argument("--agent", action="append", choices=AGENTS, help="本项目启用的 Agent，可重复传入。")
    parser.add_argument(
        "--capture-policy",
        choices=("explicit", "always"),
        default="explicit",
        help="主动采集策略（capture policy），默认 explicit：只通过 /prd-start 开启。",
    )
    parser.add_argument("--force", action="store_true", help="覆盖已有初始化配置（overwrite existing config）。")
    return parser.parse_args()


def write_if_missing(path: Path, content: str, force: bool = False) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def upsert_marked_block(path: Path, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    start = existing.find(PRD_BLOCK_START)
    end = existing.find(PRD_BLOCK_END)
    if start != -1 and end != -1 and end > start:
        end += len(PRD_BLOCK_END)
        updated = existing[:start].rstrip() + "\n" + block.strip() + "\n" + existing[end:].lstrip()
    else:
        prefix = existing.rstrip()
        updated = (prefix + "\n\n" if prefix else "") + block.strip() + "\n"
    path.write_text(updated, encoding="utf-8")


def adapter_block(agent: str) -> str:
    adapter = ADAPTER_FILES[agent][1]
    adapter_path = skill_root() / adapter
    if adapter_path.exists():
        return adapter_path.read_text(encoding="utf-8")
    return "\n".join(
        [
            PRD_BLOCK_START,
            "# PRD Helper Skill Instructions",
            "",
            "本项目使用 PRD Helper Skill Kit 处理产品上下文。",
            "完整规则见已安装 Skill 的 `SKILL.md`。",
            PRD_BLOCK_END,
            "",
        ]
    )


def install_codex_plugin(skill_root: Path, docs_root: str) -> Path:
    """Install PRD Helper as a Codex plugin to ~/.codex/plugins/prd-helper/."""
    from lib.discovery import find_codex_home
    from lib.constants import CODEX_PLUGIN_DIR

    codex_home = find_codex_home()
    plugin_dest = codex_home / CODEX_PLUGIN_DIR

    plugin_src = skill_root / "support" / "adapters" / "codex" / "plugin"
    if not plugin_src.exists():
        print(f"Codex plugin source not found: {plugin_src}")
        return plugin_dest

    # Remove existing plugin if present
    if plugin_dest.exists():
        shutil.rmtree(plugin_dest)

    # Copy plugin structure
    shutil.copytree(plugin_src, plugin_dest)

    # Replace template variables in command files
    for md_file in (plugin_dest / "commands").glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        content = content.replace("{skill_root}", str(skill_root))
        content = content.replace("{docs_root}", docs_root)
        md_file.write_text(content, encoding="utf-8")

    print(f"Codex plugin installed: {plugin_dest}")
    return plugin_dest


def install_agent_configs(project: Path, agents: list[str]) -> list[Path]:
    written: list[Path] = []
    seen_targets: set[Path] = set()
    for agent in agents:
        if agent not in ADAPTER_FILES:
            continue
        target_name, _ = ADAPTER_FILES[agent]
        target = project / target_name
        if target in seen_targets:
            continue
        seen_targets.add(target)
        upsert_marked_block(target, adapter_block(agent))
        written.append(target)
    return written


def _command_script_kind(name: str) -> str:
    if name == "prd-helper":
        return "setup"
    if name == "prd-remove":
        return "remove"
    return "collect"


def claude_command_content(name: str, description: str, docs_root: str) -> str:
    setup_script = Path(__file__).resolve()
    collect_root = f"{docs_root}/01-collect"
    script_kind = _command_script_kind(name)

    if script_kind == "setup":
        command = f'python3 "{setup_script}" --project . --docs-root {docs_root} --agent claude-code'
    elif script_kind == "remove":
        command = f'python3 "{_REMOVE_SCRIPT}" --project . --agent claude-code'
    else:
        command = (
            f'python3 "{_COLLECT_CONTROL}" {name.removeprefix("prd-")} '
            f"--root {collect_root} --project . --docs-root {docs_root} --agent claude-code"
        )

    if script_kind in ("setup", "remove"):
        return "\n".join(
            [
                "---",
                f"description: {description}",
                "---",
                "",
                f"# /{name}",
                "",
                "请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。",
                "",
                "执行：",
                "",
                "```bash",
                command,
                "```",
                "",
                "执行后用简短中文说明结果；如果用户使用英文，则用英文说明。",
                "",
            ]
        )

    return "\n".join(
        [
            "---",
            f"description: {description}",
            "---",
            "",
            f"# /{name}",
            "",
            "请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。",
            "",
            "如果项目尚未初始化，先执行：",
            "",
            "```bash",
            f'python3 "{setup_script}" --project . --docs-root {docs_root} --agent claude-code',
            "```",
            "",
            "然后执行本命令对应操作：",
            "",
            "```bash",
            command,
            "```",
            "",
            "执行后用简短中文说明结果；如果用户使用英文，则用英文说明。",
            "",
        ]
    )


def install_claude_commands(project: Path, docs_root: str) -> list[Path]:
    commands_dir = project / ".claude" / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for command in ALL_COMMANDS:
        target = commands_dir / f"{command.name}.md"
        # 优先使用手写命令文件（如 prd-discuss 的多步骤 prompt）
        handwritten = _SKILL_ROOT / "commands" / f"{command.name}.md"
        if handwritten.exists():
            target.write_text(handwritten.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            target.write_text(
                claude_command_content(command.name, command.zh_description, docs_root),
                encoding="utf-8",
            )
        written.append(target)
    return written


def main() -> int:
    args = parse_args()
    project = Path(args.project).resolve()
    docs_root = project / args.docs_root
    agents = args.agent or ["codex", "claude-code", "trae", "trae-cn"]

    for relative in MODULE_DIRS:
        (docs_root / relative).mkdir(parents=True, exist_ok=True)

    config = (
        f"# PRD Helper Config\n\n"
        f"- docs_root: {args.docs_root}\n"
        f"- enabled_agents: {', '.join(agents)}\n"
        f"- capture_policy: {args.capture_policy}\n"
        f"- commands:\n{command_markdown_list(GENERATED_COMMANDS)}\n"
    )
    write_if_missing(docs_root / "prd-helper-config.md", config, args.force)

    collect_dir = docs_root / "01-collect"
    if not (collect_dir / "collect-state.md").exists():
        write_collect_state(
            collect_dir,
            {
                "capture_mode": "off",
                "session_id": "",
                "active_root": f"{args.docs_root}/01-collect/active",
                "passive_root": f"{args.docs_root}/01-collect/passive",
                "turn_count": "0",
            },
        )
    write_if_missing(collect_dir / "source-index.md", INDEX_HEADER, False)

    write_if_missing(
        collect_dir / "README.md",
        "# PRD Helper - 采集（Collect）\n\n保存原始产品上下文，包括 Agent 会话、被动材料、元信息和状态。\n",
        False,
    )

    prd_readme_template = skill_root() / "modules" / "collect" / "templates" / "prd-helper-readme-template.md"
    if prd_readme_template.exists():
        write_if_missing(docs_root / "README.md", prd_readme_template.read_text(encoding="utf-8"), False)

    config_files = install_agent_configs(project, agents)
    command_files: list[Path] = []
    if "claude-code" in agents:
        command_files = install_claude_commands(project, args.docs_root)

    codex_plugin_dir: Path | None = None
    if "codex" in agents:
        codex_plugin_dir = install_codex_plugin(_SKILL_ROOT, args.docs_root)

    print(f"PRD Helper 初始化完成（setup complete）：{docs_root}")
    if config_files:
        print("已写入 Agent 配置：")
        for path in config_files:
            print(f"- {path}")
    if command_files:
        print("已写入 Claude Code 斜杠命令：")
        for path in command_files:
            print(f"- {path}")
    if codex_plugin_dir:
        print(f"已安装 Codex 插件：{codex_plugin_dir}")
    print("下一步：准备采集产品上下文时，在 Agent 中发送 /prd-start；Hook 会在 start 时启用，在 stop 时清理。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
