"""Check 脚本共享框架 — 输出格式和 Markdown 生成。"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional
import re


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

    def __init__(self, output_dir: Path, title: str | None = None, template_path: Path | None = None):
        self._output_dir = output_dir
        self._template_path = template_path
        self._template_sections = _parse_template_sections(template_path) if template_path else {}
        self._template_conclusion = _parse_template_conclusion(template_path) if template_path else None
        self._title = title or _parse_template_title(template_path) or "检查"
        self._meta: list[tuple[str, str]] = []
        self._sections: list[tuple[str, list[tuple[bool, str]]]] = []
        self._conclusion: Optional[tuple[bool, str, str, str, str]] = None

    def add_meta(self, key: str, value: str) -> None:
        self._meta.append((key, value))

    def add_section(self, heading: str, items: list[tuple[bool, str]]) -> None:
        self._sections.append((heading, items))

    def add_template_section(self, heading: str, status_by_item: dict[str, bool]) -> None:
        template_items = self._template_sections.get(heading, [])
        if not template_items:
            raise KeyError(f"Template section not found: {heading}")
        self.add_section(heading, [(status_by_item.get(item, False), item) for item in template_items])

    def add_conclusion(
        self,
        can_proceed: bool,
        reason: str,
        heading: str | None = None,
        prompt: str | None = None,
        proceed_label: str | None = None,
    ) -> None:
        if self._template_conclusion:
            template_heading, template_prompt, template_proceed = self._template_conclusion
            heading = heading or template_heading
            prompt = template_prompt if prompt is None else prompt
            proceed_label = proceed_label or template_proceed
        heading = heading or "结论"
        prompt = prompt or ""
        proceed_label = proceed_label or "可以进入下一阶段"
        self._conclusion = (can_proceed, reason, heading, prompt, proceed_label)

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
            can_proceed, reason, heading, prompt, proceed_label = self._conclusion
            lines.append(f"## {heading}")
            lines.append("")
            if prompt:
                lines.append(prompt)
                lines.append("")
            lines.append(f"- [{'x' if can_proceed else ' '}] {proceed_label}")
            lines.append(f"- [{'x' if not can_proceed else ' '}] 不可以")
            lines.append(f"- 原因：{reason}")
            lines.append("")

        check_file.write_text("\n".join(lines), encoding="utf-8")
        return check_file


def _parse_template_title(template_path: Path | None) -> str:
    if not template_path or not template_path.exists():
        return ""
    for line in template_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line.removeprefix("# ").strip()
    return ""


def _parse_template_sections(template_path: Path | None) -> dict[str, list[str]]:
    if not template_path or not template_path.exists():
        return {}
    sections: dict[str, list[str]] = {}
    current = ""
    for line in template_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current = line.removeprefix("## ").strip()
            sections.setdefault(current, [])
            continue
        match = re.match(r"^- \[ \] (.+)$", line)
        if current and match:
            item = match.group(1).strip()
            if item not in ("可以", "不可以"):
                sections[current].append(item)
    return sections


def _parse_template_conclusion(template_path: Path | None) -> tuple[str, str, str] | None:
    if not template_path or not template_path.exists():
        return None
    lines = template_path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("## ") or "结论" not in line:
            continue
        heading = line.removeprefix("## ").strip()
        prompt = ""
        proceed_label = "可以"
        for following in lines[index + 1:]:
            if following.startswith("## "):
                break
            if following.startswith("- [ ] "):
                label = following.removeprefix("- [ ] ").strip()
                if label != "不可以":
                    proceed_label = label
                    break
            if following.strip() and not following.startswith("- "):
                prompt = following.strip()
        return heading, prompt, proceed_label
    return None
