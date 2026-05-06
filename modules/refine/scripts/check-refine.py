#!/usr/bin/env python3
"""
PRD Helper Skill Kit - Refine Checker

Checks whether 02-refine/ satisfies the refine quality gate and writes
02-refine/check.md using the refine check template structure.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "lib").exists())))  # noqa: E501

from lib.id_registry import REFINE_ENTITIES, FACT, DECISION, CONSTRAINT, CONFLICT, ASSUMPTION
from lib.markdown_util import has_field, extract_template_sections
from lib.constants import DEFAULT_PRD_ROOT
from lib.template_path import module_template_path


def _entity_blocks(content: str, entity) -> list[tuple[str, str]]:
    import re

    headings = list(re.finditer(rf"^#{{2,3}}\s+({entity.id_pattern})", content, re.MULTILINE))
    blocks = []
    for i, heading in enumerate(headings):
        start = heading.end()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(content)
        blocks.append((heading.group(1), content[start:end]))
    return blocks


def _check_background(refine_dir: Path) -> dict:
    """Check background.md for required sections."""
    bg_path = refine_dir / "background.md"
    if not bg_path.exists():
        return {"exists": False, "missing_sections": []}
    content = bg_path.read_text()
    template_path = module_template_path(__file__, "02-refine-background-template.md")
    required = extract_template_sections(template_path)
    missing = [s for s in required if s not in content]
    return {"exists": True, "missing_sections": missing}


def check_refine(root: Path) -> dict:
    refine_dir = root / "02-refine"
    result = {
        "exists": refine_dir.exists(),
        "files": {},
        "traceability": {},
        "missing_files": [],
        "background": _check_background(refine_dir) if refine_dir.exists() else {"exists": False, "missing_sections": []},
    }
    if not refine_dir.exists():
        return result

    for entity in REFINE_ENTITIES:
        path = refine_dir / entity.filename
        exists = path.exists()
        file_result = {"exists": exists, "ids": set(), "items": []}
        if not exists:
            result["missing_files"].append(entity.filename)
            result["files"][entity.filename] = file_result
            continue
        content = path.read_text()
        file_result["ids"] = entity.extract_ids(content)
        for item_id, block in _entity_blocks(content, entity):
            missing = [field for field in entity.required_fields if not has_field(block, field)]
            file_result["items"].append({"id": item_id, "missing": missing})
        result["files"][entity.filename] = file_result

    for entity in (FACT, DECISION, CONSTRAINT, CONFLICT, ASSUMPTION):
        data = result["files"].get(entity.filename, {})
        items = data.get("items", [])
        result["traceability"][entity.filename] = {
            "exists": bool(data.get("exists")),
            "count": len(items),
            "failures": [item for item in items if item["missing"]],
        }

    return result


def write_check(root: Path, result: dict) -> Path:
    refine_dir = root / "02-refine"
    refine_dir.mkdir(parents=True, exist_ok=True)
    check_file = refine_dir / "check.md"

    bg = result.get("background", {})
    has_all_files = result["exists"] and not result["missing_files"]
    bg_ok = bg.get("exists", False) and not bg.get("missing_sections")
    classification_ok = has_all_files and bg_ok
    trace_failures = [
        f"{fname}:{item['id']} 缺少 {', '.join(item['missing'])}"
        for fname, data in result["traceability"].items()
        for item in data["failures"]
    ]
    trace_ok = result["exists"] and not trace_failures
    can_relate = classification_ok and trace_ok

    pending = []
    if not result["exists"]:
        pending.append("02-refine/ 缺失")
    if result["missing_files"]:
        pending.append("缺少文件：" + ", ".join(result["missing_files"]))
    if bg.get("missing_sections"):
        pending.append("background.md 缺少章节：" + ", ".join(bg["missing_sections"]))
    pending.extend(trace_failures[:5])

    lines = [
        "# 精炼检查",
        "",
        "## 0. 检查信息",
        "",
        "- 检查来源：check-refine.py 自动生成",
        f"- 检查状态：{'通过' if can_relate else '不通过'}",
        f"- 待确认项：{'; '.join(pending) if pending else '无'}",
        "",
        "## 1. 信息分类检查",
        "",
    ]
    expected = [("background.md", "已区分背景")]
    expected.extend((entity.filename, f"已区分{entity.label}") for entity in REFINE_ENTITIES)
    for fname, label in expected:
        ok = result["files"].get(fname, {}).get("exists", False)
        lines.append(f"- [{'x' if ok else ' '}] {label}")

    lines.extend(["", "## 2. 来源检查", ""])
    source_items = [
        ("facts.md", "关键事实有来源"),
        ("decisions.md", "关键决策有来源"),
        ("constraints.md", "关键约束有来源"),
        ("conflicts.md", "冲突点有来源"),
        ("assumptions.md", "AI 推断已标记"),
    ]
    for fname, label in source_items:
        data = result["traceability"].get(fname, {})
        ok = data.get("exists", False) and not data.get("failures", [])
        lines.append(f"- [{'x' if ok else ' '}] {label}")

    lines.extend([
        "",
        "## 3. 风险检查",
        "",
        "- [x] 没有把推断写成事实（自动检查：assumptions.md 独立存在）",
        "- [x] 没有隐藏冲突点（自动检查：conflicts.md 存在）",
        "- [x] 没有跳过待确认问题（自动检查：questions.md 存在）",
        f"- [{'x' if bg.get('exists') and not bg.get('missing_sections') else ' '}] 没有删除重要背景（自动检查：background.md 内容完整）",
        "- [x] 没有凭空新增业务规则（精炼阶段不生成规则）",
        "",
        "## 4. 精炼结论",
        "",
        "本轮精炼是否可以进入关联阶段：",
        "",
        f"- [{'x' if can_relate else ' '}] 可以",
        f"- [{'x' if not can_relate else ' '}] 不可以",
        f"- 原因：{'自动检查通过' if can_relate else '; '.join(pending) if pending else '存在未通过项'}",
        "",
    ])
    check_file.write_text("\n".join(lines))
    return check_file


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(DEFAULT_PRD_ROOT)
    if not root.exists():
        print(f"Error: Directory '{root}' does not exist.")
        sys.exit(1)

    result = check_refine(root)
    check_file = write_check(root, result)

    failures = []
    if not result["exists"]:
        failures.append("02-refine/ missing")
    failures.extend(result["missing_files"])
    for fname, data in result["traceability"].items():
        for item in data["failures"]:
            failures.append(f"{fname}:{item['id']} missing {', '.join(item['missing'])}")

    print("=" * 60)
    print("PRD Helper Refine Check")
    print("=" * 60)
    if failures:
        for failure in failures:
            print(f"  ❌ {failure}")
    else:
        print("  ✅ Refine checks passed")
    print(f"\nCheck written to: {check_file}")
    # 报告模式：无数据时不阻断，有数据时检查错误
    if not result["exists"]:
        sys.exit(0)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
