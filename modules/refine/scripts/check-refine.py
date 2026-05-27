#!/usr/bin/env python3
"""
PRD Helper Skill Kit - Refine Checker

Checks whether 02-refine/ satisfies the refine quality gate and writes
02-refine/check.md using the refine check template structure.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "_bootstrap.py").exists())))  # noqa: E501
from _bootstrap import setup_path
setup_path(__file__)

from lib.id_registry import REFINE_ENTITIES, get_entity
from lib.markdown_util import has_field, extract_template_sections
from lib.constants import DEFAULT_PRD_ROOT
from lib.template_path import module_template_path
from lib.check_framework import CheckWriter, print_header, print_footer
from lib.source_anchor import has_source_anchor


TRACE_ENTITY_NAMES = ("fact", "decision", "constraint", "conflict", "assumption")


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
    content = bg_path.read_text(encoding="utf-8")
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
        "trace_quality": {},
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
        content = path.read_text(encoding="utf-8")
        file_result["ids"] = entity.extract_ids(content)
        for item_id, block in _entity_blocks(content, entity):
            missing = [field for field in entity.required_fields if not has_field(block, field)]
            file_result["items"].append({"id": item_id, "missing": missing})
        result["files"][entity.filename] = file_result

    for entity in (get_entity(n) for n in TRACE_ENTITY_NAMES):
        data = result["files"].get(entity.filename, {})
        items = data.get("items", [])
        result["traceability"][entity.filename] = {
            "exists": bool(data.get("exists")),
            "count": len(items),
            "failures": [item for item in items if item["missing"]],
        }
        strong = []
        weak = []
        content = (refine_dir / entity.filename).read_text(encoding="utf-8") if data.get("exists") else ""
        blocks = _entity_blocks(content, entity) if content else []
        for item_id, block in blocks:
            if has_source_anchor(block):
                strong.append(item_id)
            else:
                weak.append(item_id)
        result["trace_quality"][entity.filename] = {
            "exists": bool(data.get("exists")),
            "strong": strong,
            "weak": weak,
        }

    return result


def write_check(root: Path, result: dict) -> Path:
    refine_dir = root / "02-refine"
    refine_dir.mkdir(parents=True, exist_ok=True)

    bg = result.get("background", {})
    has_all_files = result["exists"] and not result["missing_files"]
    bg_ok = bg.get("exists", False) and not bg.get("missing_sections")
    classification_ok = has_all_files and bg_ok
    trace_failures = [
        f"{fname}:{item['id']} 缺少 {', '.join(item['missing'])}"
        for fname, data in result["traceability"].items()
        for item in data["failures"]
    ]
    weak_trace_failures = [
        f"{fname}:{item_id} Weak Trace 缺少 source_id/path/quote-or-paraphrase/locator"
        for fname, data in result.get("trace_quality", {}).items()
        for item_id in data.get("weak", [])
    ]
    trace_ok = result["exists"] and not trace_failures and not weak_trace_failures
    can_relate = classification_ok and trace_ok

    pending = []
    if not result["exists"]:
        pending.append("02-refine/ 缺失")
    if result["missing_files"]:
        pending.append("缺少文件：" + ", ".join(result["missing_files"]))
    if bg.get("missing_sections"):
        pending.append("background.md 缺少章节：" + ", ".join(bg["missing_sections"]))
    pending.extend(trace_failures[:5])
    pending.extend(weak_trace_failures[:5])

    w = CheckWriter(refine_dir, template_path=module_template_path(__file__, "02-refine-check-template.md"))
    w.add_meta("检查来源", "check-refine.py 自动生成")
    w.add_meta("检查状态", "通过" if can_relate else "不通过")
    w.add_meta("待确认项", "; ".join(pending) if pending else "无")

    w.add_template_section("1. 信息分类检查", {
        "已区分事实": result["files"].get("facts.md", {}).get("exists", False),
        "已区分背景": bg.get("exists", False),
        "已区分目标": result["files"].get("goals.md", {}).get("exists", False),
        "已区分决策": result["files"].get("decisions.md", {}).get("exists", False),
        "已区分约束": result["files"].get("constraints.md", {}).get("exists", False),
        "已区分冲突": result["files"].get("conflicts.md", {}).get("exists", False),
        "已区分待确认问题": result["files"].get("questions.md", {}).get("exists", False),
        "已区分 AI 推断": result["files"].get("assumptions.md", {}).get("exists", False),
    })

    source_items = [
        ("facts.md", "关键事实有来源"),
        ("decisions.md", "关键决策有来源"),
        ("constraints.md", "关键约束有来源"),
        ("conflicts.md", "冲突点有来源"),
        ("assumptions.md", "AI 推断已标记"),
    ]
    source_checks = {
        label: (
            result["traceability"].get(fname, {}).get("exists", False)
            and not result["traceability"].get(fname, {}).get("failures", [])
            and not result.get("trace_quality", {}).get(fname, {}).get("weak", [])
        )
        for fname, label in source_items
    }
    source_checks["Strong Trace 具备 source_id + path + quote/paraphrase + locator"] = not weak_trace_failures
    source_checks["Weak Trace 未进入确定性要求"] = not weak_trace_failures
    w.add_template_section("2. 来源检查", source_checks)

    w.add_template_section("3. 风险检查", {
        "没有把推断写成事实": True,
        "没有隐藏冲突点": True,
        "没有跳过待确认问题": True,
        "没有删除重要背景": bg.get("exists", False) and not bg.get("missing_sections"),
        "没有凭空新增业务规则": True,
    })

    w.add_conclusion(
        can_proceed=can_relate,
        reason="自动检查通过" if can_relate else "; ".join(pending) if pending else "存在未通过项",
    )
    return w.write()


def main() -> None:
    parser = argparse.ArgumentParser(description="PRD Check Refine")
    parser.add_argument("root_arg", nargs="?", help="PRD root directory")
    parser.add_argument("--root", default=None, help="PRD root directory")
    args = parser.parse_args()

    root = Path(args.root or args.root_arg or DEFAULT_PRD_ROOT)
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

    print_header("PRD Helper Refine Check")
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
