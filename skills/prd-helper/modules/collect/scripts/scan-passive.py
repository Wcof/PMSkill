#!/usr/bin/env python3
"""
PRD Helper - Scan Passive

Scans the passive/ directory, computes content hashes, and updates source-index.md.
Does NOT modify any original files in passive/.

Usage:
    python scan-passive.py [--root <collect-root>]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "lib").exists())))  # noqa: E501

from lib.collect_writer import SUPPORTED_PASSIVE_EXTENSIONS, scan_passive_sources
from lib.source_index import ensure_index
from lib.constants import DEFAULT_COLLECT_ROOT


def main():
    parser = argparse.ArgumentParser(description="PRD Scan Passive")
    parser.add_argument("--root", default=DEFAULT_COLLECT_ROOT, help="Collect root directory")
    args = parser.parse_args()

    root = Path(args.root)
    passive_dir = root / "passive"

    if not passive_dir.exists():
        passive_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created passive directory: {passive_dir}")

    ensure_index(root)
    result = scan_passive_sources(root)
    for entry in result.entries:
        print(
            f"Indexed: {entry['path']} "
            f"({entry['source_type']}, metadata: {entry['metadata_status']})"
        )

    print(f"\nScan complete. New files indexed: {result.added_count}")
    print(f"Supported passive extensions: {', '.join(sorted(SUPPORTED_PASSIVE_EXTENSIONS))}")


if __name__ == "__main__":
    main()
