#!/usr/bin/env python3
"""通过 Agent 指令初始化 PRD Helper 项目配置。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.source_index import INDEX_HEADER


AGENTS = ("codex", "claude-code", "trae", "trae-cn")
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

    print(f"PRD Helper 初始化完成（setup complete）：{docs_root}")
    print("下一步：准备采集产品上下文时，在 Agent 中发送 /prd-start。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
