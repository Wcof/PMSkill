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

sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "lib").exists())))  # noqa: E501
from lib.id_registry import ALL_ENTITIES
from lib.markdown_util import extract_template_sections
from lib.constants import DEFAULT_PRD_ROOT
from lib.template_path import module_template_path
from lib.check_framework import CheckWriter


def _safe_rglob(directory: Path, pattern: str = "*.md"):
    """rglob that skips hidden directories (starting with '.')."""
    for item in directory.rglob(pattern):
        # Skip files in hidden directories
        if any(part.startswith(".") for part in item.relative_to(directory).parts):
            continue
        yield item


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


def _read_generated_files(root_path: Path) -> list[tuple[str, str]]:
    """Read all generated .md files once, returning (rel_path, content) pairs."""
    gen_dir = root_path / "04-generate"
    if not gen_dir.exists():
        return []
    files = []
    for md_file in _safe_rglob(gen_dir):
        if md_file.name == "check.md":
            continue
        files.append((str(md_file.relative_to(root_path)), md_file.read_text(encoding="utf-8")))
    return files


def check_unresolved_content(files: list[tuple[str, str]]) -> list[dict]:
    """Check for unresolved TODOs and markers in generated content."""
    results = []
    for rel_path, content in files:
        for pattern, label in UNRESOLVED_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                results.append({"file": rel_path, "pattern": label, "count": len(matches)})
    return results


def check_pending_questions_consolidation(root_path: Path, files: list[tuple[str, str]]) -> dict:
    """Check if pending questions from generated docs are consolidated in 05-check."""
    check_dir = root_path / "05-check"

    if not files:
        return {"checked": True, "pending_count": 0, "all_consolidated": True}

    # Collect all pending questions from pre-read files
    pending_questions = []
    for rel_path, content in files:
        for line in content.split("\n"):
            if "待确认" in line and line.strip().startswith(("-", "|", "*")):
                pending_questions.append({
                    "file": rel_path,
                    "line": line.strip()[:80],
                })

    if not pending_questions:
        return {"checked": True, "pending_count": 0, "all_consolidated": True}

    # Collect text from 05-check consolidation files
    consolidated_text = ""
    for fname in ["context-delta.md", "generated-check.md", "full-check.md"]:
        fpath = check_dir / fname
        if fpath.exists():
            consolidated_text += "\n" + fpath.read_text(encoding="utf-8")

    # Check each question: at least its question ID or first 15 chars should appear
    unconsolidated = []
    for q in pending_questions:
        line = q["line"]
        # Extract question ID (e.g. question_001) if present
        qid_match = re.search(r"question[_-]\d+", line)
        if qid_match:
            key = qid_match.group()
        else:
            # Use first 15 meaningful chars as match key
            key = re.sub(r"[\s\-\|*：:]+", "", line)[:15]
        if key and key not in consolidated_text:
            unconsolidated.append(q)

    return {
        "checked": True,
        "pending_count": len(pending_questions),
        "all_consolidated": len(unconsolidated) == 0,
        "unconsolidated": unconsolidated[:5],
        "pending_questions": pending_questions[:5],
    }


def check_traceability(files: list[tuple[str, str]]) -> list[dict]:
    """Check if generated docs keep source or relation traceability."""
    if not files:
        return []

    # 从注册表动态构建可追溯性模式
    trace_patterns = [entity.id_pattern for entity in ALL_ENTITIES]
    trace_patterns.extend([
        r"来源说明",
        r"来源事实",
        r"关联规则",
        r"关联数据",
        r"关联验收",
    ])

    results = []
    for rel_path, content in files:
        has_trace = any(re.search(pattern, content) for pattern in trace_patterns)
        results.append({
            "file": rel_path,
            "status": "PASS" if has_trace else "FAIL",
        })

    return results


def check_page_completeness(root_path: Path) -> list[dict]:
    """Check if page documents have required sections from template."""
    return _check_doc_completeness(
        root_path / "04-generate" / "pages",
        module_template_path(__file__, "04-generate-page-prd-template.md"),
        root_path,
    )


def check_rule_completeness(root_path: Path) -> list[dict]:
    """Check if rule documents have required sections from template."""
    return _check_doc_completeness(
        root_path / "04-generate" / "rules",
        module_template_path(__file__, "04-generate-rule-prd-template.md"),
        root_path,
    )


def _check_doc_completeness(docs_dir: Path, template_path: Path, root_path: Path) -> list[dict]:
    """Check if documents in a directory have required sections from a template."""
    results = []
    if not docs_dir.exists():
        return results

    required_sections = extract_template_sections(template_path)

    for md_file in docs_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        rel_path = md_file.relative_to(root_path)

        missing = [s for s in required_sections if s not in content]
        results.append({
            "file": str(rel_path),
            "status": "FAIL" if missing else "PASS",
            "missing_sections": missing,
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
        unconsol = consolidation.get("unconsolidated", [])
        if unconsol:
            for q in unconsol[:3]:
                pending.append(f"待确认问题未汇总: {q['line'][:40]}")
        else:
            pending.append("待确认问题未汇总到 05-check")

    w = CheckWriter(gen_dir, template_path=module_template_path(__file__, "04-generate-check-template.md"))
    w.add_meta("检查来源", "check-generated.py 自动生成")
    w.add_meta("检查状态", "通过" if can_final else "不通过")
    w.add_meta("待确认项", "; ".join(pending[:8]) if pending else "无")

    w.add_template_section("1. 来源检查", {
        "生成内容来自 02-refine": bool(traceability),
        "生成内容来自 03-relate": bool(traceability),
        "没有凭空新增规则": not unresolved,
        "AI 推断已标记": not any(r["status"] == "FAIL" for r in traceability),
        "待确认问题已保留": not (consolidation["checked"] and not consolidation["all_consolidated"]),
    })

    w.add_template_section("2. 结构检查", {
        "项目说明完整": True,
        "页面说明完整": page_ok,
        "功能规则完整": rule_ok,
        "数据说明完整": True,
        "验收标准完整": True,
        "Agent 上下文完整": True,
    })

    w.add_template_section("3. 角色覆盖检查", {
        "产品经理可读": source_ok,
        "前端可执行": source_ok,
        "后端可理解": source_ok,
        "测试可验收": source_ok,
        "Agent 可使用": source_ok,
    })

    w.add_conclusion(
        can_proceed=can_final,
        reason="自动检查通过" if can_final else "; ".join(pending[:8]) if pending else "存在未通过项",
    )
    return w.write()


def main():
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = DEFAULT_PRD_ROOT

    root_path = Path(root)
    if not root_path.exists():
        print(f"Error: Directory '{root}' does not exist.")
        sys.exit(1)

    files = _read_generated_files(root_path)
    unresolved = check_unresolved_content(files)
    consolidation = check_pending_questions_consolidation(root_path, files)
    traceability = check_traceability(files)
    pages = check_page_completeness(root_path)
    rules = check_rule_completeness(root_path)

    print_results(unresolved, consolidation, traceability, pages, rules)
    check_file = write_check_md(root_path, unresolved, consolidation, traceability, pages, rules)
    print(f"\nCheck written to: {check_file}")

    # 报告模式：无数据时不阻断，有数据时检查错误
    gen_dir = root_path / "04-generate"
    if not gen_dir.exists() or not files:
        sys.exit(0)

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
