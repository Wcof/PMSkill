#!/usr/bin/env python3
"""通过 Agent 指令初始化 PRD Helper 项目配置。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.source_index import INDEX_HEADER


AGENTS = ("codex", "claude-code", "trae", "trae-cn")
PRD_BLOCK_START = "<!-- PRD-HELPER:START -->"
PRD_BLOCK_END = "<!-- PRD-HELPER:END -->"
ADAPTER_FILES = {
    "codex": ("AGENTS.md", "support/adapters/codex/AGENTS.md"),
    "claude-code": ("CLAUDE.md", "support/adapters/claude-code/CLAUDE.md"),
    "trae": ("project_rules.md", "support/adapters/trae/project_rules.md"),
    "trae-cn": ("project_rules.md", "support/adapters/trae/project_rules.md"),
}
CLAUDE_COMMANDS = {
    "prd-setup": {
        "description": "初始化 PRD Helper 项目配置",
        "script": "setup",
        "command": "",
    },
    "prd-start": {
        "description": "开启 PRD Helper 主动采集",
        "script": "collect",
        "command": "start",
    },
    "prd-pause": {
        "description": "暂停 PRD Helper 主动采集",
        "script": "collect",
        "command": "pause",
    },
    "prd-resume": {
        "description": "恢复 PRD Helper 主动采集",
        "script": "collect",
        "command": "resume",
    },
    "prd-stop": {
        "description": "停止 PRD Helper 主动采集并生成摘要",
        "script": "collect",
        "command": "stop",
    },
    "prd-status": {
        "description": "查看 PRD Helper 采集状态",
        "script": "collect",
        "command": "status",
    },
    "prd-remove": {
        "description": "卸载 PRD Helper 并清理 Agent 配置",
        "script": "remove",
        "command": "",
    },
}
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
    collect_script = setup_script.parent / "collect-control.py"
    remove_script = setup_script.parent / "remove-prd-helper.py"
    collect_root = f"{docs_root}/01-collect"
    description = meta["description"]

    if meta["script"] == "setup":
        command = f'python3 "{setup_script}" --project . --docs-root {docs_root} --agent claude-code'
    elif meta["script"] == "remove":
        command = f'python3 "{remove_script}" --project . --agent claude-code'
    else:
        command = (
            f'python3 "{collect_script}" {meta["command"]} '
            f"--root {collect_root} --agent claude-code"
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

    collect_state = "\n".join(
        [
            "# PRD Helper 采集状态（Collect State）",
            "",
            "| Key | Value |",
            "| --- | --- |",
            "| capture_mode | off |",
            "| session_id |  |",
            f"| active_root | {args.docs_root}/01-collect/active |",
            f"| passive_root | {args.docs_root}/01-collect/passive |",
            "| last_captured_at |  |",
            "| turn_count | 0 |",
            "",
        ]
    )
    write_if_missing(docs_root / "01-collect" / "collect-state.md", collect_state, False)
    write_if_missing(docs_root / "01-collect" / "source-index.md", INDEX_HEADER, False)
    write_if_missing(docs_root / "01-collect" / "README.md", "# 01 采集（Collect）\n\n- `active/`：Agent 在 `/prd-start` 后写入主动会话采集内容（active conversation captures）。\n- `passive/`：人工投放会议纪要、评审记录、旧 PRD、客户反馈等被动材料（passive materials）。\n", False)

    config_files = install_agent_configs(project, agents)
    command_files: list[Path] = []
    if "claude-code" in agents:
        command_files = install_claude_commands(project, args.docs_root)

    print(f"PRD Helper 初始化完成（setup complete）：{docs_root}")
    if config_files:
        print("已写入 Agent 配置：")
        for path in config_files:
            print(f"- {path}")
    if command_files:
        print("已写入 Claude Code 斜杠命令：")
        for path in command_files:
            print(f"- {path}")
    print("下一步：准备采集产品上下文时，在 Agent 中发送 /prd-start。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
