#!/usr/bin/env python3
"""
PRD Helper Skill Kit - Relation Checker

Checks whether relations are properly established between
facts, pages, features, rules, data, and acceptance.

Usage:
    python check-relations.py [docs/prd-helper/root]

Output:
    Prints check results to stdout.
"""

import os
import re
import sys
from pathlib import Path


def extract_ids(content: str, prefix: str) -> set[str]:
    """Extract IDs with given prefix from markdown content."""
    pattern = rf"{prefix}[_-]\d+"
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
    facts_file = root_path / "02-refine" / "facts.md"
    if not facts_file.exists():
        return {"exists": False, "count": 0, "with_source": 0, "with_status": 0}

    content = facts_file.read_text()

    # Extract facts from both table rows and section headers
    rows = extract_table_rows(content)
    fact_ids_from_table = set()
    for r in rows:
        for v in r.values():
            found = re.findall(r"fact[_-]\d+", str(v))
            fact_ids_from_table.update(found)

    # Also extract from section headers like "### fact_001"
    fact_ids_from_headers = set(re.findall(r"fact[_-]\d+", content))

    all_fact_ids = fact_ids_from_table | fact_ids_from_headers

    with_source = sum(1 for r in rows if r.get("来源", r.get("来源材料", "")).strip() not in ("", "-"))
    with_status = sum(1 for r in rows if r.get("状态", "").strip() not in ("", "-"))

    return {
        "exists": True,
        "count": max(len(all_fact_ids), len(rows)),
        "with_source": with_source,
        "with_status": with_status,
        "fact_ids": all_fact_ids,
    }


def check_relations(root_path: Path) -> dict:
    """Check relation files for completeness."""
    rel_dir = root_path / "03-relate"
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
        # Count sections (## headers) as well for non-table formats
        sections = re.findall(r"^##\s+\w+_\d+", content, re.MULTILINE)
        entry_count = max(len(rows), len(sections))
        file_results[f] = {"exists": True, "count": entry_count}

    return {"exists": True, "files": file_results}


def check_fact_coverage(root_path: Path) -> dict:
    """Check if all facts have page or feature associations."""
    facts_file = root_path / "02-refine" / "facts.md"
    rel_dir = root_path / "03-relate"

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


def check_context_map(root_path: Path) -> dict:
    """Check context-map.md for facts, pages, features, rules, data, acceptance coverage."""
    context_map = root_path / "03-relate" / "context-map.md"
    if not context_map.exists():
        return {"exists": False}

    content = context_map.read_text()

    has_facts = bool(re.search(r"fact[_-]\d+", content))
    has_pages = bool(re.search(r"page[_-]\d+", content))
    has_features = bool(re.search(r"feature[_-]\d+", content))
    has_rules = bool(re.search(r"rule[_-]\d+", content))
    has_data = bool(re.search(r"data[_-]\d+", content))
    has_acceptance = bool(re.search(r"acceptance[_-]\d+", content))

    return {
        "exists": True,
        "has_facts": has_facts,
        "has_pages": has_pages,
        "has_features": has_features,
        "has_rules": has_rules,
        "has_data": has_data,
        "has_acceptance": has_acceptance,
    }


def print_results(facts: dict, relations: dict, coverage: dict, context_map: dict):
    print("=" * 60)
    print("PRD Helper Relation Check")
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
        print("  ❌ 03-relate/ not found")
    print()

    # Coverage check
    print("--- Fact Coverage ---")
    if coverage["checked"]:
        print(f"  Total facts: {coverage['total_facts']}")
        print(f"  Mapped: {coverage['mapped']}")
        if coverage["unmapped"]:
            print(f"  ❌ Unmapped facts: {', '.join(coverage['unmapped'])}")
        else:
            print(f"  ✅ All facts mapped")
    else:
        print("  ⚠️  Could not check coverage")
    print()

    # Context map check
    print("--- Context Map ---")
    if context_map["exists"]:
        checks = [
            ("facts", context_map["has_facts"]),
            ("pages", context_map["has_pages"]),
            ("features", context_map["has_features"]),
            ("rules", context_map["has_rules"]),
            ("data", context_map["has_data"]),
            ("acceptance", context_map["has_acceptance"]),
        ]
        for name, present in checks:
            icon = "✅" if present else "❌"
            print(f"  {icon} Contains {name}")
    else:
        print("  ❌ context-map.md not found")
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

    facts = check_facts(root_path)
    relations = check_relations(root_path)
    coverage = check_fact_coverage(root_path)
    context_map = check_context_map(root_path)

    print_results(facts, relations, coverage, context_map)

    # Exit with non-zero if there are uncovered facts
    has_issues = False
    if coverage["checked"] and coverage["unmapped"]:
        has_issues = True

    sys.exit(1 if has_issues else 0)


if __name__ == "__main__":
    main()
