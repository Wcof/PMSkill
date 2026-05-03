#!/usr/bin/env python3
"""
PRD Helper Skill Kit - Structure Checker

Checks whether the PRD helper directory structure is complete
and key files exist.

Usage:
    python check-structure.py [docs/prd-helper/root]

Output:
    Prints check results to stdout.
    Optionally writes to 05-check/structure-check-result.md
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.constants import REQUIRED_GENERATED_SUBDIRS, REQUIRED_GENERATED_FILES
from lib.id_registry import REFINE_ENTITIES, RELATE_ENTITIES
from lib.constants import DEFAULT_PRD_ROOT

# Required directories
REQUIRED_DIRS = [
    "01-collect",
    "02-refine",
    "03-relate",
    "04-generate",
    "05-check",
]

# Required files per directory
REQUIRED_FILES = {
    "01-collect": ["check.md"],
    "02-refine": [
        "background.md",
        *(entity.filename for entity in REFINE_ENTITIES),
        "check.md",
    ],
    "03-relate": [
        *(entity.filename for entity in RELATE_ENTITIES),
        "context-map.md",
        "check.md",
    ],
    "04-generate": ["check.md"],
    "05-check": [
        "full-check.md",
        "gap-check.md",
        "relation-check.md",
        "source-check.md",
        "generated-check.md",
        "context-delta.md",
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
    for subdir in REQUIRED_GENERATED_SUBDIRS:
        dir_path = root_path / "04-generate" / subdir
        exists = dir_path.exists()
        results.append({
            "type": "directory",
            "path": f"04-generate/{subdir}",
            "exists": exists,
            "status": "PASS" if exists else "FAIL",
        })

    # Check generated files
    for subdir, files in REQUIRED_GENERATED_FILES.items():
        for f in files:
            file_path = root_path / "04-generate" / subdir / f
            exists = file_path.exists()
            results.append({
                "type": "file",
                "path": f"04-generate/{subdir}/{f}",
                "exists": exists,
                "status": "PASS" if exists else "FAIL",
            })

    return results


def print_results(results: list[dict]):
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    total = len(results)

    print("=" * 60)
    print("PRD Helper Structure Check")
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
        root = DEFAULT_PRD_ROOT

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
