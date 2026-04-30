#!/usr/bin/env python3
"""
PRD Context Skill Kit - Relation Checker

Checks whether relations are properly established between
facts, pages, features, rules, data, and acceptance.

Usage:
    python check-relations.py [docs/prd-context/root]

Output:
    Prints check results to stdout.
"""

import os
import re
import sys
from pathlib import Path


def extract_ids(content: str, prefix: str) -> set[str]:
    """Extract IDs with given prefix from markdown content."""
    pattern = rf"{prefix}-\d+"
    return set(re.findall(pattern, content))


def extract_table_rows(content: str) -> list[dict]:
    """Extract data from markdown tables."""
    rows = []
    lines = content.split("\n")
    headers = []

    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            continue

        cells = [c.strip() for c in line.split("|")[1:-1]]

        # Skip separator rows
        if all(set(c) <= {"-", ":", " "} for c in cells):
            continue

        if not headers:
            headers = cells
        else:
            if len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))

    return rows


def check_facts(root_path: Path) -> dict:
    """Check facts.md for completeness."""
    facts_file = root_path / "02-refined" / "facts.md"
    if not facts_file.exists():
        return {"exists": False, "count": 0, "with_source": 0, "with_status": 0}

    content = facts_file.read_text()
    rows = extract_table_rows(content)

    with_source = sum(1 for r in rows if r.get("来源", "").strip() not in ("", "-"))
    with_status = sum(1 for r in rows if r.get("状态", "").strip() not in ("", "-"))

    return {
        "exists": True,
        "count": len(rows),
        "with_source": with_source,
        "with_status": with_status,
    }


def check_relations(root_path: Path) -> dict:
    """Check relation files for completeness."""
    rel_dir = root_path / "03-relations"
    if not rel_dir.exists():
        return {"exists": False, "files": {}}

    files_to_check = [
        "page-map.md",
        "feature-map.md",
        "rule-map.md",
        "data-map.md",
        "acceptance-map.md",
    ]

    file_results = {}
    for f in files_to_check:
        file_path = rel_dir / f
        if not file_path.exists():
            file_results[f] = {"exists": False, "count": 0}
            continue

        content = file_path.read_text()
        rows = extract_table_rows(content)
        file_results[f] = {"exists": True, "count": len(rows)}

    return {"exists": True, "files": file_results}


def check_page_coverage(root_path: Path) -> dict:
    """Check if all facts have page or feature associations."""
    facts_file = root_path / "02-refined" / "facts.md"
    rel_dir = root_path / "03-relations"

    if not facts_file.exists() or not rel_dir.exists():
        return {"checked": False}

    facts_content = facts_file.read_text()
    fact_ids = extract_ids(facts_content, "fact")

    # Check across all relation files
    relation_files = [
        "page-map.md",
        "feature-map.md",
        "rule-map.md",
        "data-map.md",
        "acceptance-map.md",
        "context-map.md",
    ]

    mapped_facts = set()
    for f in relation_files:
        rel_file = rel_dir / f
        if rel_file.exists():
            content = rel_file.read_text()
            mapped_facts |= extract_ids(content, "fact")

    unmapped = fact_ids - mapped_facts

    return {
        "checked": True,
        "total_facts": len(fact_ids),
        "mapped": len(mapped_facts),
        "unmapped": list(unmapped),
    }


def check_isolation(root_path: Path) -> dict:
    """Check for isolated pages, rules, and features."""
    rel_dir = root_path / "03-relations"
    isolated = {"pages": [], "rules": [], "features": []}

    # Check page-map
    page_map = rel_dir / "page-map.md"
    if page_map.exists():
        content = page_map.read_text()
        rows = extract_table_rows(content)
        for r in rows:
            page = r.get("关联页面", r.get("页面", "")).strip()
            fact = r.get("来源事实", r.get("fact_id", "")).strip()
            if page and not fact:
                isolated["pages"].append(page)

    # Check rule-map
    rule_map = rel_dir / "rule-map.md"
    if rule_map.exists():
        content = rule_map.read_text()
        rows = extract_table_rows(content)
        for r in rows:
            rule = r.get("关联规则", r.get("规则", "")).strip()
            feature = r.get("关联功能", r.get("功能", "")).strip()
            if rule and not feature:
                isolated["rules"].append(rule)

    return isolated


def print_results(facts: dict, relations: dict, coverage: dict, isolation: dict):
    print("=" * 60)
    print("PRD Context Relation Check")
    print("=" * 60)
    print()

    # Facts check
    print("--- Facts ---")
    if facts["exists"]:
        print(f"  Total facts: {facts['count']}")
        print(f"  With source: {facts['with_source']}")
        print(f"  With status: {facts['with_status']}")
    else:
        print("  ❌ facts.md not found")
    print()

    # Relations check
    print("--- Relations ---")
    if relations["exists"]:
        for fname, data in relations["files"].items():
            icon = "✅" if data["exists"] else "❌"
            count = data["count"] if data["exists"] else 0
            print(f"  {icon} {fname}: {count} entries")
    else:
        print("  ❌ 03-relations/ not found")
    print()

    # Coverage check
    print("--- Fact Coverage ---")
    if coverage["checked"]:
        print(f"  Total facts: {coverage['total_facts']}")
        print(f"  Mapped to pages: {coverage['mapped']}")
        if coverage["unmapped"]:
            print(f"  ❌ Unmapped facts: {', '.join(coverage['unmapped'])}")
        else:
            print(f"  ✅ All facts mapped to pages")
    else:
        print("  ⚠️  Could not check coverage")
    print()

    # Isolation check
    print("--- Isolation Check ---")
    has_isolation = False
    for category, items in isolation.items():
        if items:
            has_isolation = True
            print(f"  ❌ Isolated {category}: {', '.join(items)}")
    if not has_isolation:
        print("  ✅ No isolated items found")
    print()

    print("=" * 60)


def main():
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = "docs/prd-context"

    root_path = Path(root)
    if not root_path.exists():
        print(f"Error: Directory '{root}' does not exist.")
        sys.exit(1)

    facts = check_facts(root_path)
    relations = check_relations(root_path)
    coverage = check_page_coverage(root_path)
    isolation = check_isolation(root_path)

    print_results(facts, relations, coverage, isolation)

    # Exit with non-zero if there are uncovered facts or isolation issues
    has_issues = False
    if coverage["checked"] and coverage["unmapped"]:
        has_issues = True
    for items in isolation.values():
        if items:
            has_issues = True

    sys.exit(1 if has_issues else 0)


if __name__ == "__main__":
    main()
