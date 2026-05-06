"""Check 脚本共享框架 — 输出格式和 Markdown 生成。"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional


def print_header(title: str) -> None:
    print("=" * 60)
    print(title)
    print("=" * 60)
    print()


def print_footer() -> None:
    print("=" * 60)


def print_section(title: str, items: list[tuple[bool, str]]) -> None:
    print(f"--- {title} ---")
    for passed, text in items:
        icon = "✅" if passed else "❌"
        print(f"  {icon} {text}")
    print()


def exit_with_status(has_failures: bool) -> None:
    sys.exit(1 if has_failures else 0)


class CheckWriter:
    """构建 check.md 文件的构建器。

    使用模式:
        w = CheckWriter(root / "02-refine", "精炼检查")
        w.add_meta("检查来源", "check-refine.py 自动生成")
        w.add_section("1. 文件检查", [
            (True, "facts.md 存在"),
            (False, "decisions.md 缺失"),
        ])
        w.add_conclusion(can_proceed=False, reason="decisions.md 缺失")
        w.write()
    """

    def __init__(self, output_dir: Path, title: str):
        self._output_dir = output_dir
        self._title = title
        self._meta: list[tuple[str, str]] = []
        self._sections: list[tuple[str, list[tuple[bool, str]]]] = []
        self._conclusion: Optional[tuple[bool, str]] = None

    def add_meta(self, key: str, value: str) -> None:
        self._meta.append((key, value))

    def add_section(self, heading: str, items: list[tuple[bool, str]]) -> None:
        self._sections.append((heading, items))

    def add_conclusion(self, can_proceed: bool, reason: str) -> None:
        self._conclusion = (can_proceed, reason)

    def write(self) -> Path:
        self._output_dir.mkdir(parents=True, exist_ok=True)
        check_file = self._output_dir / "check.md"

        lines = [f"# {self._title}", ""]

        # Section 0: metadata
        lines.append("## 0. 检查信息")
        lines.append("")
        for key, value in self._meta:
            lines.append(f"- {key}：{value}")
        lines.append("")

        # Sections 1-N
        for heading, items in self._sections:
            lines.append(f"## {heading}")
            lines.append("")
            for passed, text in items:
                mark = "x" if passed else " "
                lines.append(f"- [{mark}] {text}")
            lines.append("")

        # Conclusion
        if self._conclusion:
            can_proceed, reason = self._conclusion
            lines.append("## 结论")
            lines.append("")
            lines.append(f"- [{'x' if can_proceed else ' '}] 可以进入下一阶段")
            lines.append(f"- [{'x' if not can_proceed else ' '}] 不可以")
            lines.append(f"- 原因：{reason}")
            lines.append("")

        check_file.write_text("\n".join(lines))
        return check_file
