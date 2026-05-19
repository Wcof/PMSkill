#!/usr/bin/env python3
"""清理 Agent 配置文件中的 PRD Helper 配置块。"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


START = "<!-- PRD-HELPER:START -->"
END = "<!-- PRD-HELPER:END -->"

AGENT_FILES = {
    "codex": ["AGENTS.md"],
    "claude-code": ["CLAUDE.md"],
    "trae": [
        "project_rules.md",
        ".trae/project_rules.md",
        ".trae/rules/project_rules.md",
    ],
    "trae-cn": [
        "project_rules.md",
        ".trae/project_rules.md",
        ".trae/rules/project_rules.md",
    ],
}


def remove_marked_block(text: str) -> tuple[str, bool]:
    pattern = re.compile(
        rf"\n?{re.escape(START)}.*?{re.escape(END)}\n?",
        flags=re.DOTALL,
    )
    updated, count = pattern.subn("\n", text)
    updated = re.sub(r"\n{3,}", "\n\n", updated).strip()
    if updated:
        updated += "\n"
    return updated, count > 0


def clean_file(path: Path, dry_run: bool) -> bool:
    if not path.exists():
        return False
    original = path.read_text(encoding="utf-8")
    updated, changed = remove_marked_block(original)
    if changed and not dry_run:
        path.write_text(updated, encoding="utf-8")
    return changed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="清理 PRD Helper Agent 配置块（Clean agent config blocks）", add_help=False)
    parser._optionals.title = "可选参数（optional arguments）"
    parser.add_argument("-h", "--help", action="help", help="显示帮助信息并退出（show help and exit）。")
    parser.add_argument(
        "--project",
        default=".",
        help="目标项目根目录（project root），默认当前目录。",
    )
    parser.add_argument(
        "--agent",
        action="append",
        choices=sorted(AGENT_FILES),
        help="要清理配置的 Agent，可重复传入；默认所有支持的 Agent。",
    )
    parser.add_argument("--dry-run", action="store_true", help="只报告不写入文件（dry run）。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.project).resolve()
    agents = args.agent or sorted(AGENT_FILES)
    changed_paths: list[Path] = []

    for agent in agents:
        for relative in AGENT_FILES[agent]:
            path = root / relative
            if clean_file(path, args.dry_run):
                changed_paths.append(path)

    if changed_paths:
        action = "将清理（Would clean）" if args.dry_run else "已清理（Cleaned）"
        for path in changed_paths:
            print(f"{action}: {path}")
    else:
        print("未发现 PRD Helper 配置块。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
