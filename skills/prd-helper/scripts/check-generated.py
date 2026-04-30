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

import os
import re
import sys
from pathlib import Path


# Required generated subdirectories and files
REQUIRED_STRUCTURE = {
    "overview": ["project-overview.md"],
    "pages": [],  # At least one file
    "rules": [],  # At least one file
    "data": [],   # At least one file
    "acceptance": [],  # At least one file
    "agent-context": [
        "frontend-context.md",
        "backend-context.md",
        "test-context.md",
        "product-review-context.md",
    ],
}

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


def check_directory_structure(root_path: Path) -> list[dict]:
    """Check if generated directory structure is complete."""
    results = []
    gen_dir = root_path / "04-generate"

    if not gen_dir.exists():
        return [{"check": "04-generate exists", "status": "FAIL", "detail": "Directory not found"}]

    for subdir, required_files in REQUIRED_STRUCTURE.items():
        dir_path = gen_dir / subdir

        if not dir_path.exists():
            results.append({
                "check": f"04-generate/{subdir} exists",
                "status": "FAIL",
                "detail": "Directory not found",
            })
            continue

        results.append({
            "check": f"04-generate/{subdir} exists",
            "status": "PASS",
            "detail": "",
        })

        # Check for files
        md_files = list(dir_path.glob("*.md"))
        if required_files:
            for f in required_files:
                file_path = dir_path / f
                exists = file_path.exists()
                results.append({
                    "check": f"04-generate/{subdir}/{f} exists",
                    "status": "PASS" if exists else "FAIL",
                    "detail": "" if exists else "File not found",
                })
        else:
            if len(md_files) == 0:
                results.append({
                    "check": f"04-generate/{subdir} has content",
                    "status": "WARN",
                    "detail": "No .md files found",
                })
            else:
                results.append({
                    "check": f"04-generate/{subdir} has content",
                    "status": "PASS",
                    "detail": f"{len(md_files)} file(s)",
                })

    return results


def check_unresolved_content(root_path: Path) -> list[dict]:
    """Check for unresolved TODOs and markers in generated content."""
    results = []
    gen_dir = root_path / "04-generate"

    if not gen_dir.exists():
        return results

    for md_file in gen_dir.rglob("*.md"):
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


def check_page_completeness(root_path: Path) -> list[dict]:
    """Check if page documents have required sections."""
    results = []
    pages_dir = root_path / "04-generate" / "pages"

    if not pages_dir.exists():
        return results

    required_sections = [
        "页面目标",
        "页面区域",
        "字段",
        "操作",
        "状态",
        "验收",
    ]

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
                "status": "WARN",
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
    """Check if rule documents have required sections."""
    results = []
    rules_dir = root_path / "04-generate" / "rules"

    if not rules_dir.exists():
        return results

    required_sections = [
        "前置条件",
        "执行步骤",
        "异常",
        "权限",
    ]

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
                "status": "WARN",
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
    structure: list[dict],
    unresolved: list[dict],
    consolidation: dict,
    pages: list[dict],
    rules: list[dict],
):
    print("=" * 60)
    print("PRD Helper Generated Content Check")
    print("=" * 60)
    print()

    # Structure check
    print("--- Structure ---")
    for r in structure:
        icon = "✅" if r["status"] == "PASS" else "❌" if r["status"] == "FAIL" else "⚠️"
        detail = f" ({r['detail']})" if r['detail'] else ""
        print(f"  {icon} {r['check']}{detail}")
    print()

    # Unresolved content
    print("--- Unresolved Content ---")
    if unresolved:
        for r in unresolved:
            print(f"  ⚠️  {r['file']}: {r['pattern']} x{r['count']}")
    else:
        print("  ✅ No unresolved content found")
    print()

    # Pending questions consolidation
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

    # Page completeness
    print("--- Page Completeness ---")
    if pages:
        for r in pages:
            icon = "✅" if r["status"] == "PASS" else "⚠️"
            missing = f" (missing: {', '.join(r['missing_sections'])})" if r["missing_sections"] else ""
            print(f"  {icon} {r['file']}{missing}")
    else:
        print("  ℹ️  No pages to check")
    print()

    # Rule completeness
    print("--- Rule Completeness ---")
    if rules:
        for r in rules:
            icon = "✅" if r["status"] == "PASS" else "⚠️"
            missing = f" (missing: {', '.join(r['missing_sections'])})" if r["missing_sections"] else ""
            print(f"  {icon} {r['file']}{missing}")
    else:
        print("  ℹ️  No rules to check")
    print()

    print("=" * 60)


def main():
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = "docs/prd-helper"

    root_path = Path(root)
    if not root_path.exists():
        print(f"Error: Directory '{root}' does not exist.")
        sys.exit(1)

    structure = check_directory_structure(root_path)
    unresolved = check_unresolved_content(root_path)
    consolidation = check_pending_questions_consolidation(root_path)
    pages = check_page_completeness(root_path)
    rules = check_rule_completeness(root_path)

    print_results(structure, unresolved, consolidation, pages, rules)


if __name__ == "__main__":
    main()
