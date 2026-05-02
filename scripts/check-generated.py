#!/usr/bin/env python3
"""
PRD Helper Skill Kit - Generated Content Checker

Checks whether generated documents are complete and contain
no unresolved TODOs or unconfirmed items. Also checks whether
pending questions are properly consolidated in final check or context-delta.

Usage:
    python check-generated.py [docs/prd-helper/root]

Output:
    Prints check results to stdout.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.id_registry import ALL_ENTITIES
from lib.markdown_util import extract_template_sections
from lib.paths import DEFAULT_PRD_ROOT

# Patterns that indicate unresolved content
UNRESOLVED_PATTERNS = [
    (r"<!--\s*TODO", "<!-- TODO"),
    (r"<!--\s*FIXME", "<!-- FIXME"),
    (r"<!--\s*TBD", "<!-- TBD"),
    (r"\[TODO\]", "[TODO]"),
    (r"\[TBD\]", "[TBD]"),
    (r"\[待确认\]", "[待确认]"),
    (r"\[未确认\]", "[未确认]"),
    (r"<!--\s*待确认\s*-->", "<!-- 待确认 -->"),
    (r"<!--\s*无来源\s*-->", "<!-- 无来源 -->"),
]


def check_unresolved_content(root_path: Path) -> list[dict]:
    """Check for unresolved TODOs and markers in generated content."""
    results = []
    gen_dir = root_path / "04-generate"

    if not gen_dir.exists():
        return results

    for md_file in gen_dir.rglob("*.md"):
        if md_file == gen_dir / "check.md":
            continue
        content = md_file.read_text()
        rel_path = md_file.relative_to(root_path)

        for pattern, label in UNRESOLVED_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                results.append({
                    "file": str(rel_path),
                    "pattern": label,
                    "count": len(matches),
                })

    return results


def check_pending_questions_consolidation(root_path: Path) -> dict:
    """Check if pending questions from generated docs are consolidated in 05-check."""
    gen_dir = root_path / "04-generate"
    check_dir = root_path / "05-check"

    if not gen_dir.exists():
        return {"checked": False, "reason": "04-generate not found"}

    # Collect all pending questions from generated docs
    pending_questions = []
    for md_file in gen_dir.rglob("*.md"):
        content = md_file.read_text()
        rel_path = str(md_file.relative_to(root_path))
        # Find "待确认" entries
        for line in content.split("\n"):
            if "待确认" in line and line.strip().startswith(("-", "|", "*")):
                pending_questions.append({
                    "file": rel_path,
                    "line": line.strip()[:80],
                })

    if not pending_questions:
        return {"checked": True, "pending_count": 0, "all_consolidated": True}

    # Check if context-delta.md or generated-check.md mentions these
    consolidated_files = []
    for fname in ["context-delta.md", "generated-check.md", "full-check.md"]:
        fpath = check_dir / fname
        if fpath.exists():
            consolidated_files.append(fpath.read_text())

    all_text = "\n".join(consolidated_files)
    has_consolidation = "待确认" in all_text or "question" in all_text.lower()

    return {
        "checked": True,
        "pending_count": len(pending_questions),
        "all_consolidated": has_consolidation,
        "pending_questions": pending_questions[:5],  # Show first 5
    }


def check_traceability(root_path: Path) -> list[dict]:
    """Check if generated docs keep source or relation traceability."""
    results = []
    gen_dir = root_path / "04-generate"

    if not gen_dir.exists():
        return results

    # 从注册表动态构建可追溯性模式
    trace_patterns = [entity.id_pattern for entity in ALL_ENTITIES]
    trace_patterns.extend([
        r"来源说明",
        r"来源事实",
        r"关联规则",
        r"关联数据",
        r"关联验收",
    ])

    for md_file in gen_dir.rglob("*.md"):
        if md_file == gen_dir / "check.md":
            continue
        content = md_file.read_text()
        rel_path = md_file.relative_to(root_path)
        has_trace = any(re.search(pattern, content) for pattern in trace_patterns)
        results.append({
            "file": str(rel_path),
            "status": "PASS" if has_trace else "FAIL",
        })

    return results


def check_page_completeness(root_path: Path) -> list[dict]:
    """Check if page documents have required sections from template."""
    results = []
    pages_dir = root_path / "04-generate" / "pages"

    if not pages_dir.exists():
        return results

    # 从模板动态获取必填章节
    template_path = Path(__file__).parent.parent / "modules" / "generate" / "templates" / "04-generate-page-prd-template.md"
    required_sections = extract_template_sections(template_path)

    for md_file in pages_dir.glob("*.md"):
        content = md_file.read_text()
        rel_path = md_file.relative_to(root_path)

        missing = []
        for section in required_sections:
            if section not in content:
                missing.append(section)

        if missing:
            results.append({
                "file": str(rel_path),
                "status": "FAIL",
                "missing_sections": missing,
            })
        else:
            results.append({
                "file": str(rel_path),
                "status": "PASS",
                "missing_sections": [],
            })

    return results


def check_rule_completeness(root_path: Path) -> list[dict]:
    """Check if rule documents have required sections from template."""
    results = []
    rules_dir = root_path / "04-generate" / "rules"

    if not rules_dir.exists():
        return results

    # 从模板动态获取必填章节
    template_path = Path(__file__).parent.parent / "modules" / "generate" / "templates" / "04-generate-rule-prd-template.md"
    required_sections = extract_template_sections(template_path)

    for md_file in rules_dir.glob("*.md"):
        content = md_file.read_text()
        rel_path = md_file.relative_to(root_path)

        missing = []
        for section in required_sections:
            if section not in content:
                missing.append(section)

        if missing:
            results.append({
                "file": str(rel_path),
                "status": "FAIL",
                "missing_sections": missing,
            })
        else:
            results.append({
                "file": str(rel_path),
                "status": "PASS",
                "missing_sections": [],
            })

    return results


def print_results(
    unresolved: list[dict],
    consolidation: dict,
    traceability: list[dict],
    pages: list[dict],
    rules: list[dict],
):
    print("=" * 60)
    print("PRD Helper Generated Content Check")
    print("=" * 60)
    print()

    print("--- Unresolved Content ---")
    if unresolved:
        for r in unresolved:
            print(f"  ⚠️  {r['file']}: {r['pattern']} x{r['count']}")
    else:
        print("  ✅ No unresolved content found")
    print()

    print("--- Pending Questions Consolidation ---")
    if consolidation["checked"]:
        if consolidation["pending_count"] == 0:
            print("  ✅ No pending questions in generated docs")
        elif consolidation["all_consolidated"]:
            print(f"  ✅ {consolidation['pending_count']} pending questions found, consolidated in 05-check")
        else:
            print(f"  ❌ {consolidation['pending_count']} pending questions NOT consolidated in 05-check")
    else:
        print("  ⚠️  Could not check consolidation")
    print()

    print("--- Traceability ---")
    if traceability:
        for r in traceability:
            icon = "✅" if r["status"] == "PASS" else "❌"
            print(f"  {icon} {r['file']}")
    else:
        print("  ℹ️  No generated files to check")
    print()

    print("--- Page Completeness ---")
    if pages:
        for r in pages:
            icon = "✅" if r["status"] == "PASS" else "❌"
            missing = f" (missing: {', '.join(r['missing_sections'])})" if r["missing_sections"] else ""
            print(f"  {icon} {r['file']}{missing}")
    else:
        print("  ℹ️  No pages to check")
    print()

    print("--- Rule Completeness ---")
    if rules:
        for r in rules:
            icon = "✅" if r["status"] == "PASS" else "❌"
            missing = f" (missing: {', '.join(r['missing_sections'])})" if r["missing_sections"] else ""
            print(f"  {icon} {r['file']}{missing}")
    else:
        print("  ℹ️  No rules to check")
    print()

    print("=" * 60)


def write_check_md(
    root_path: Path,
    unresolved: list[dict],
    consolidation: dict,
    traceability: list[dict],
    pages: list[dict],
    rules: list[dict],
) -> Path:
    """Write 04-generate/check.md using the generate check template structure."""
    gen_dir = root_path / "04-generate"
    gen_dir.mkdir(parents=True, exist_ok=True)
    check_file = gen_dir / "check.md"

    source_ok = (
        not unresolved
        and not any(r["status"] == "FAIL" for r in traceability)
        and not (consolidation["checked"] and not consolidation["all_consolidated"])
    )
    page_ok = bool(pages) and not any(r["status"] == "FAIL" for r in pages)
    rule_ok = bool(rules) and not any(r["status"] == "FAIL" for r in rules)
    can_final = source_ok and page_ok and rule_ok

    pending = []
    pending.extend(f"{r['file']} 缺少来源追溯" for r in traceability if r["status"] == "FAIL")
    pending.extend(f"{r['file']} 存在未解决标记" for r in unresolved)
    pending.extend(f"{r['file']} 缺少章节" for r in pages if r["status"] == "FAIL")
    pending.extend(f"{r['file']} 缺少章节" for r in rules if r["status"] == "FAIL")
    if consolidation["checked"] and not consolidation["all_consolidated"]:
        pending.append("待确认问题未汇总到 05-check")

    lines = [
        "# 生成检查",
        "",
        "## 0. 检查信息",
        "",
        "- 检查来源：check-generated.py 自动生成",
        f"- 检查状态：{'通过' if can_final else '不通过'}",
        f"- 待确认项：{'; '.join(pending[:8]) if pending else '无'}",
        "",
        "## 1. 来源检查",
        "",
        f"- [{'x' if traceability else ' '}] 生成内容来自 02-refine",
        f"- [{'x' if traceability else ' '}] 生成内容来自 03-relate",
        f"- [{'x' if not unresolved else ' '}] 没有凭空新增规则",
        f"- [{'x' if not any(r['status'] == 'FAIL' for r in traceability) else ' '}] AI 推断已标记",
        f"- [{'x' if not (consolidation['checked'] and not consolidation['all_consolidated']) else ' '}] 待确认问题已保留",
        "",
        "## 2. 结构检查",
        "",
        "- [x] 结构完整性由 check-structure.py 独立负责",
        f"- [{'x' if page_ok else ' '}] 页面说明完整",
        f"- [{'x' if rule_ok else ' '}] 功能规则完整",
        "- [x] 数据说明结构由 check-structure.py 独立负责",
        "- [x] 验收标准结构由 check-structure.py 独立负责",
        "- [x] Agent 上下文结构由 check-structure.py 独立负责",
        "",
        "## 3. 角色覆盖检查",
        "",
        f"- [{'x' if source_ok else ' '}] 产品经理可读",
        f"- [{'x' if source_ok else ' '}] 前端可执行",
        f"- [{'x' if source_ok else ' '}] 后端可理解",
        f"- [{'x' if source_ok else ' '}] 测试可验收",
        f"- [{'x' if source_ok else ' '}] Agent 可使用",
        "",
        "## 4. 生成结论",
        "",
        "本轮生成是否可以进入最终检查：",
        "",
        f"- [{'x' if can_final else ' '}] 可以",
        f"- [{'x' if not can_final else ' '}] 不可以",
        f"- 原因：{'自动检查通过' if can_final else '; '.join(pending[:8]) if pending else '存在未通过项'}",
        "",
    ]
    check_file.write_text("\n".join(lines))
    return check_file


def main():
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = DEFAULT_PRD_ROOT

    root_path = Path(root)
    if not root_path.exists():
        print(f"Error: Directory '{root}' does not exist.")
        sys.exit(1)

    unresolved = check_unresolved_content(root_path)
    consolidation = check_pending_questions_consolidation(root_path)
    traceability = check_traceability(root_path)
    pages = check_page_completeness(root_path)
    rules = check_rule_completeness(root_path)

    print_results(unresolved, consolidation, traceability, pages, rules)
    check_file = write_check_md(root_path, unresolved, consolidation, traceability, pages, rules)
    print(f"\nCheck written to: {check_file}")

    has_unresolved = len(unresolved) > 0
    has_consolidation_fail = consolidation["checked"] and not consolidation["all_consolidated"]
    has_traceability_fail = any(r["status"] == "FAIL" for r in traceability)
    has_page_fail = any(r["status"] == "FAIL" for r in pages)
    has_rule_fail = any(r["status"] == "FAIL" for r in rules)

    if (
        has_unresolved
        or has_consolidation_fail
        or has_traceability_fail
        or has_page_fail
        or has_rule_fail
    ):
        sys.exit(1)


if __name__ == "__main__":
    main()
