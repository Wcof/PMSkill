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
from datetime import datetime
from pathlib import Path

# Add scripts/ to path for lib imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.state import read_collect_state, write_collect_state
from lib.time_util import TZ, now_iso
from lib.hash_util import file_hash
from lib.source_index import ensure_index, read_indexed_paths, append_index
from lib.paths import DEFAULT_COLLECT_ROOT
from lib.metadata import metadata_status_for_text


SUPPORTED_EXTENSIONS = {
    ".md": "markdown",
    ".txt": "text",
    ".docx": "word",
    ".pdf": "pdf",
    ".doc": "word",
    ".csv": "csv",
    ".json": "json",
    ".html": "html",
    ".htm": "html",
}


def main():
    parser = argparse.ArgumentParser(description="PRD Scan Passive")
    parser.add_argument("--root", default=DEFAULT_COLLECT_ROOT, help="Collect root directory")
    args = parser.parse_args()

    root = Path(args.root)
    passive_dir = root / "passive"

    if not passive_dir.exists():
        passive_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created passive directory: {passive_dir}")

    state = read_collect_state(root)
    ensure_index(root)
    indexed = read_indexed_paths(root)

    new_count = 0
    passive_count = int(state.get("passive_source_count", "0"))

    for fpath in sorted(passive_dir.iterdir()):
        if fpath.is_dir():
            continue

        rel_path = str(fpath.relative_to(root))

        # Skip already indexed
        if rel_path in indexed:
            continue

        ext = fpath.suffix.lower()
        source_type = SUPPORTED_EXTENSIONS.get(ext, "unknown")
        c_hash = file_hash(fpath)
        source_id = f"passive-{fpath.stem}-{datetime.now(TZ).strftime('%Y%m%d')}"

        # Check metadata status from bilingual front matter or markdown fields.
        metadata_status = "missing"
        if ext in (".md", ".txt"):
            try:
                content = fpath.read_text()
                metadata_status = metadata_status_for_text(content)
            except Exception:
                pass

        entry = {
            "source_id": source_id,
            "source_time": now_iso(),
            "source_type": source_type,
            "source_channel": "passive",
            "path": rel_path,
            "content_hash": c_hash,
            "metadata_status": metadata_status,
            "noise_hint": "none",
            "status": "collected",
        }

        append_index(root, entry)
        new_count += 1
        passive_count += 1
        print(f"Indexed: {rel_path} ({source_type}, metadata: {metadata_status})")

    # Update state
    if new_count > 0:
        state["passive_source_count"] = str(passive_count)
        state["total_sources"] = str(int(state.get("total_sources", "0")) + new_count)
        write_collect_state(root, state)

    print(f"\nScan complete. New files indexed: {new_count}")
    print(f"Total passive sources: {passive_count}")


if __name__ == "__main__":
    main()
