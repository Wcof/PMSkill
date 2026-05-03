#!/usr/bin/env python3
"""通过 Agent 指令初始化 PRD Helper 项目配置。"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.constants import COMMAND_NAMES
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

# 从 COMMAND_NAMES 和命名规则推导初始化后生成的命令元数据。
# /prd-helper 是根 Skill 入口，不在这里生成，避免覆盖安装器注册的入口。
_COLLECT_DESCRIPTIONS = {
    "start": "开启 PRD Helper 主动采集",
    "pause": "暂停 PRD Helper 主动采集",
    "resume": "恢复 PRD Helper 主动采集",
    "stop": "停止 PRD Helper 主动采集并生成摘要",
    "status": "查看 PRD Helper 采集状态",
}
CLAUDE_COMMANDS = {}
for _name in COMMAND_NAMES:
    _action = _name.removeprefix("prd-")
    if _action == "remove":
        CLAUDE_COMMANDS[_name] = {"description": "卸载 PRD Helper 并清理 Agent 配置", "script": "remove", "command": ""}
    else:
        CLAUDE_COMMANDS[_name] = {"description": _COLLECT_DESCRIPTIONS[_action], "script": "collect", "command": _action}
_SCRIPT_DIR = Path(__file__).resolve().parent
_SKILL_ROOT = _SCRIPT_DIR.parent
_COLLECT_CONTROL = _SKILL_ROOT / "modules" / "collect" / "scripts" / "collect-control.py"
_REMOVE_SCRIPT = _SCRIPT_DIR / "remove-prd-helper.py"

MODULE_DIRS = (
    "01-collect/active/sessions",
    "01-collect/passive",
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
    from lib.codex_discovery import find_codex_home
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


def claude_command_content(name: str, meta: dict[str, str], docs_root: str) -> str:
    setup_script = Path(__file__).resolve()
    collect_root = f"{docs_root}/01-collect"
    description = meta["description"]

    if meta["script"] == "setup":
        command = f'python3 "{setup_script}" --project . --docs-root {docs_root} --agent claude-code'
    elif meta["script"] == "remove":
        command = f'python3 "{_REMOVE_SCRIPT}" --project . --agent claude-code'
    else:
        command = (
            f'python3 "{_COLLECT_CONTROL}" {meta["command"]} '
            f"--root {collect_root} --project . --docs-root {docs_root} --agent claude-code"
        )

    if meta["script"] in ("setup", "remove"):
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
    for name, meta in CLAUDE_COMMANDS.items():
        target = commands_dir / f"{name}.md"
        target.write_text(claude_command_content(name, meta, docs_root), encoding="utf-8")
        written.append(target)
    return written


def main() -> int:
    args = parse_args()
    project = Path(args.project).resolve()
    docs_root = project / args.docs_root
    agents = args.agent or ["codex", "claude-code", "trae", "trae-cn"]

    for relative in MODULE_DIRS:
        (docs_root / relative).mkdir(parents=True, exist_ok=True)

    config = "\n".join(
        [
            "# PRD Helper 初始化配置（Setup）",
            "",
            "| 配置项（Key） | 值（Value） |",
            "| --- | --- |",
            f"| 文档目录（docs_root） | {args.docs_root} |",
            f"| 启用 Agent（enabled_agents） | {', '.join(agents)} |",
            f"| 采集策略（capture_policy） | {args.capture_policy} |",
            "| 工作流（workflow） | 采集 Collect -> 精炼 Refine -> 关联 Relate -> 生成 Generate |",
            "",
            "## 指令（Commands）",
            "",
            "- `/prd-start`：开启显式主动采集（active capture）",
            "- `/prd-pause`：暂停主动采集",
            "- `/prd-resume`：恢复主动采集",
            "- `/prd-stop`：停止主动采集并生成采集摘要",
            "- `/prd-status`：查看采集状态",
            "- `/prd-remove`：从当前项目卸载 PRD Helper",
            "",
        ]
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

    collect_readme = "\n".join(
        [
            "# 01 Collect（信息采集）",
            "",
            "## 中文说明",
            "",
            "这是 PRD Helper 的信息采集目录。",
            "",
            "- `active/`：Agent 主动采集区，由 Agent 和脚本写入。包括 `sessions/`（会话采集）、`historical/`（历史补录）、`anomalies/`（异常材料）。",
            "- `passive/`：人工材料投放区。请把会议纪要、评审记录、旧 PRD、客户反馈、Word、PDF、Markdown、TXT 等原始材料直接放到这里。",
            "- `source-index.md`：材料索引，供下一环节精炼读取。",
            "- `collect-state.md`：采集状态，记录当前采集 session、写入路径和时间戳。",
            "- `collect-summary.md`：采集摘要，只做轻量说明，不做事实提取。",
            "- `check.md`：采集检查结果。",
            "",
            "注意：不要改写 `passive/` 中的原始材料。Agent 只扫描、索引和标记元信息。",
            "",
            "## English",
            "",
            "This is the PRD Helper collect directory.",
            "",
            "- `active/`: Agent-managed active capture area. Includes `sessions/` (conversation turns), `historical/` (backfilled materials), `anomalies/` (anomalous materials).",
            "- `passive/`: User-managed passive source drop zone. Put meeting notes, review records, legacy PRDs, customer feedback, Word, PDF, Markdown, TXT, and other raw materials here.",
            "- `source-index.md`: Source index for the next refine step.",
            "- `collect-state.md`: Capture state, including session, write roots, and timestamps.",
            "- `collect-summary.md`: Lightweight collection summary, not fact extraction.",
            "- `check.md`: Collect check result.",
            "",
            "Do not rewrite raw files in `passive/`. The Agent should only scan, index, and mark metadata.",
            "",
        ]
    )
    write_if_missing(collect_dir / "README.md", collect_readme, False)

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
    print("下一步：准备采集产品上下文时，在 Agent 中发送 /prd-start；Hook 会在 start/resume 时启用，在 pause/stop 时清理。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
