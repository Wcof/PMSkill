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

sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "lib").exists())))  # noqa: E501

from lib.state import read_collect_state, write_collect_state
from lib.time_util import TZ, now_iso
from lib.hash_util import file_hash
from lib.source_index import ensure_index, read_indexed_hashes_by_path, append_index_entries
from lib.constants import DEFAULT_COLLECT_ROOT
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
    indexed_hashes = read_indexed_hashes_by_path(root)

    entries = []
    passive_count = int(state.get("passive_source_count", "0"))

    for fpath in sorted(passive_dir.rglob("*")):
        if fpath.is_dir():
            continue

        rel_path = fpath.relative_to(root).as_posix()

        ext = fpath.suffix.lower()
        source_type = SUPPORTED_EXTENSIONS.get(ext, "unknown")
        c_hash = file_hash(fpath)

        # Skip unchanged files, but capture a new index row if a passive file changed.
        if c_hash in indexed_hashes.get(rel_path, set()):
            continue

        safe_stem = fpath.stem.replace("/", "-").replace("\\", "-")
        source_id = f"passive-{safe_stem}-{datetime.now(TZ).strftime('%Y%m%d')}-{c_hash.removeprefix('sha256:')}"

        # Check metadata status from bilingual front matter or markdown fields.
        metadata_status = "missing"
        if ext in (".md", ".txt"):
            try:
                content = fpath.read_text(encoding="utf-8")
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

        entries.append(entry)

    new_count = append_index_entries(root, entries)
    passive_count += new_count
    for entry in entries[:new_count]:
        print(
            f"Indexed: {entry['path']} "
            f"({entry['source_type']}, metadata: {entry['metadata_status']})"
        )

    # Update state
    if new_count > 0:
        state["passive_source_count"] = str(passive_count)
        state["total_sources"] = str(int(state.get("total_sources", "0")) + new_count)
        write_collect_state(root, state)

    print(f"\nScan complete. New files indexed: {new_count}")
    print(f"Total passive sources: {passive_count}")


if __name__ == "__main__":
    main()
