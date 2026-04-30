#!/usr/bin/env python3
"""
PRD Context Skill Kit - Structure Checker

Checks whether the PRD context directory structure is complete
and key files exist.

Usage:
    python check-structure.py [docs/prd-context/root]

Output:
    Prints check results to stdout.
    Optionally writes to 05-check/script-check-result.md
"""

import os
import sys
from pathlib import Path

# Required directories
REQUIRED_DIRS = [
    "01-sources",
    "02-refined",
    "03-relations",
    "04-generated",
    "05-check",
]

# Required files per directory
REQUIRED_FILES = {
    "01-sources": ["check.md"],
    "02-refined": [
        "facts.md",
        "decisions.md",
        "constraints.md",
        "conflicts.md",
        "questions.md",
        "assumptions.md",
        "check.md",
    ],
    "03-relations": [
        "page-map.md",
        "feature-map.md",
        "rule-map.md",
        "data-map.md",
        "acceptance-map.md",
        "context-map.md",
        "check.md",
    ],
    "04-generated": ["check.md"],
    "05-check": [
        "full-check.md",
        "gap-check.md",
        "relation-check.md",
        "generated-check.md",
        "context-delta.md",
        "next-actions.md",
    ],
}

# Required generated subdirectories
GENERATED_SUBDIRS = [
    "overview",
    "pages",
    "rules",
    "data",
    "acceptance",
    "agent-context",
]

# Required generated files
GENERATED_FILES = {
    "overview": ["project-overview.md"],
    "agent-context": [
        "frontend-context.md",
        "backend-context.md",
        "test-context.md",
        "product-review-context.md",
    ],
}


def check_structure(root: str) -> list[dict]:
    results = []
    root_path = Path(root)

    # Check main directories
    for d in REQUIRED_DIRS:
        dir_path = root_path / d
        exists = dir_path.exists()
        results.append({
            "type": "directory",
            "path": d,
            "exists": exists,
            "status": "PASS" if exists else "FAIL",
        })

    # Check required files
    for dir_name, files in REQUIRED_FILES.items():
        for f in files:
            file_path = root_path / dir_name / f
            exists = file_path.exists()
            results.append({
                "type": "file",
                "path": f"{dir_name}/{f}",
                "exists": exists,
                "status": "PASS" if exists else "FAIL",
            })

    # Check generated subdirectories
    for subdir in GENERATED_SUBDIRS:
        dir_path = root_path / "04-generated" / subdir
        exists = dir_path.exists()
        results.append({
            "type": "directory",
            "path": f"04-generated/{subdir}",
            "exists": exists,
            "status": "PASS" if exists else "FAIL",
        })

    # Check generated files
    for subdir, files in GENERATED_FILES.items():
        for f in files:
            file_path = root_path / "04-generated" / subdir / f
            exists = file_path.exists()
            results.append({
                "type": "file",
                "path": f"04-generated/{subdir}/{f}",
                "exists": exists,
                "status": "PASS" if exists else "FAIL",
            })

    return results


def print_results(results: list[dict]):
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    total = len(results)

    print("=" * 60)
    print("PRD Context Structure Check")
    print("=" * 60)
    print()

    for r in results:
        icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"  {icon} [{r['type']:10s}] {r['path']}")

    print()
    print("-" * 60)
    print(f"Total: {total} | Pass: {passed} | Fail: {failed}")
    print("-" * 60)

    return passed, failed


def write_report(results: list[dict], output_path: str):
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    total = len(results)

    lines = [
        "# Structure Check Report",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total | {total} |",
        f"| Pass | {passed} |",
        f"| Fail | {failed} |",
        "",
        "## Details",
        "",
        "| Type | Path | Status |",
        "|------|------|--------|",
    ]

    for r in results:
        icon = "PASS" if r["status"] == "PASS" else "FAIL"
        lines.append(f"| {r['type']} | {r['path']} | {icon} |")

    lines.append("")

    if failed > 0:
        lines.append("## Missing Items")
        lines.append("")
        for r in results:
            if r["status"] == "FAIL":
                lines.append(f"- {r['type']}: `{r['path']}`")
        lines.append("")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"\nReport written to: {output_path}")


def main():
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = "docs/prd-context"

    if not Path(root).exists():
        print(f"Error: Directory '{root}' does not exist.")
        sys.exit(1)

    results = check_structure(root)
    passed, failed = print_results(results)

    # Write report if 05-check exists
    check_dir = Path(root) / "05-check"
    if check_dir.exists():
        write_report(results, str(check_dir / "structure-check-result.md"))

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
