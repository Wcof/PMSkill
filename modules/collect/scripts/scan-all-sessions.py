#!/usr/bin/env python3
"""Scan all AI coding tool sessions for the current project.

Discovers and captures conversation sessions from:
- Claude Code (~/.claude/projects/)
- Cursor (~/Library/Application Support/Cursor/)
- Trae / Trae CN (~/Library/Application Support/Trae[ CN]/)
- Codex (~/.codex/sessions/)

Writes captured turns to active/sessions/ and updates source-index.md.

Usage:
    python scan-all-sessions.py [--collect-root <path>] [--project <path>] [--agent <name>]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "lib").exists())))  # noqa: E501

from lib.discovery import (
    TOOL_CONFIGS,
    discover_sessions,
    session_filename,
    write_session,
)
from lib.state import read_collect_state, write_collect_state, safe_int
from lib.source_index import read_indexed_paths, ensure_index
from lib.time_util import now_iso, now_id
from lib.constants import DEFAULT_COLLECT_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan all AI tool sessions for PRD Helper")
    parser.add_argument("--collect-root", default=DEFAULT_COLLECT_ROOT, help="Collect root directory")
    parser.add_argument("--project", default=".", help="Project root directory")
    parser.add_argument("--agent", default="multi", help="Agent name for source metadata")
    return parser.parse_args()


def ensure_collect_structure(root: Path, agent: str) -> dict:
    """Ensure collect directory structure and state file exist.

    Returns the collect state dict.
    """
    state = read_collect_state(root)
    if state:
        return state

    # Auto-create directory structure
    (root / "active" / "sessions").mkdir(parents=True, exist_ok=True)
    (root / "active" / "historical").mkdir(parents=True, exist_ok=True)
    (root / "active" / "anomalies").mkdir(parents=True, exist_ok=True)
    (root / "passive").mkdir(parents=True, exist_ok=True)
    ensure_index(root)

    # Create initial state
    session_id = f"scan-{now_id()}"
    state = {
        "capture_mode": "off",
        "active_root": str(root / "active"),
        "passive_root": str(root / "passive"),
        "session_id": session_id,
        "agent": agent,
        "started_at": now_iso(),
        "capture_scope": "full_turn",
        "turn_count": "0",
        "total_sources": "0",
        "active_source_count": "0",
        "passive_source_count": "0",
        "anomaly_count": "0",
        "possible_noise_count": "0",
    }
    write_collect_state(root, state)
    return state


def main() -> int:
    args = parse_args()
    collect_root = Path(args.collect_root)
    project = Path(args.project).resolve()

    print(f"Project: {project}")
    print(f"Collect root: {collect_root}")
    print()

    # Ensure structure exists
    state = ensure_collect_structure(collect_root, args.agent)
    indexed_paths = read_indexed_paths(collect_root)

    total_captured = 0
    total_skipped = 0

    # Discover and capture from all tools
    all_sessions = discover_sessions(str(project))

    for tool in TOOL_CONFIGS:
        sessions = all_sessions.get(tool, [])
        print(f"[{tool.title()}]")
        print(f"  Found {len(sessions)} sessions")

        captured = 0
        skipped = 0
        for session in sessions:
            if write_session(tool, session, collect_root, indexed_paths):
                captured += 1
                print(f"  Captured: {session_filename(tool, session.id)} ({len(session.turns)} turns)")
            else:
                skipped += 1

        total_captured += captured
        total_skipped += skipped
        print()

    # Update state
    state = read_collect_state(collect_root)
    state["turn_count"] = str(safe_int(state.get("turn_count")) + total_captured)
    state["active_source_count"] = str(safe_int(state.get("active_source_count")) + total_captured)
    state["total_sources"] = str(safe_int(state.get("total_sources")) + total_captured)
    state["last_collect_at"] = now_iso()
    write_collect_state(collect_root, state)

    # Summary
    print(f"{'='*40}")
    print(f"Scan complete: {total_captured} captured, {total_skipped} skipped (dedup)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
