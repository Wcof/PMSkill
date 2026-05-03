#!/usr/bin/env python3
"""Scan Codex session JSONL files and capture unrecorded conversation turns.

Usage:
    python scan-codex-sessions.py --collect-root <path> --project <path> [--agent codex] [--since <iso>] [--session-id <id>]
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# Locate project-level scripts/lib without depending on a fixed module depth.
for _parent in Path(__file__).resolve().parents:
    _scripts = _parent / "scripts"
    if (_scripts / "lib").exists():
        sys.path.insert(0, str(_scripts))
        break
else:
    raise RuntimeError("Unable to locate PRD Helper scripts/lib")

from lib.codex_discovery import find_codex_home, list_project_sessions, parse_session_jsonl, filter_turns
from lib.state import read_collect_state
from lib.hash_util import content_hash
from lib.constants import DEFAULT_COLLECT_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan Codex sessions for PRD Helper capture")
    parser.add_argument("--collect-root", default=DEFAULT_COLLECT_ROOT, help="Collect root directory")
    parser.add_argument("--project", default=".", help="Project root directory")
    parser.add_argument("--agent", default="codex", help="Agent name")
    parser.add_argument("--since", default="", help="ISO timestamp to filter from")
    parser.add_argument("--session-id", default="", help="Specific session ID to scan")
    return parser.parse_args()


def capture_turn(user_query: str, agent_answer: str, collect_root: str, project: str, agent: str) -> bool:
    """Call capture-source.py to record a single conversation turn."""
    capture_script = Path(__file__).resolve().parent / "capture-source.py"
    if not capture_script.exists():
        print(f"Error: capture script not found: {capture_script}", file=sys.stderr)
        return False

    temp_dir = Path(collect_root).parent / ".codex-scan-temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Use content hash to generate unique filename for temp files
    h = content_hash(user_query + agent_answer)[:12]
    user_file = temp_dir / f"scan-{h}-user.md"
    answer_file = temp_dir / f"scan-{h}-answer.md"

    user_file.write_text(user_query, encoding="utf-8")
    answer_file.write_text(agent_answer, encoding="utf-8")

    command = [
        sys.executable,
        str(capture_script),
        "--root",
        collect_root,
        "--agent",
        agent,
        "--user-query-file",
        str(user_file),
        "--agent-answer-file",
        str(answer_file),
    ]

    try:
        completed = subprocess.run(command, cwd=project, check=False, capture_output=True, text=True)
        if completed.returncode == 0:
            if completed.stdout:
                print(f"  {completed.stdout.strip()}")
            return True
        else:
            if completed.stderr:
                print(f"  Error: {completed.stderr.strip()}", file=sys.stderr)
            return False
    finally:
        user_file.unlink(missing_ok=True)
        answer_file.unlink(missing_ok=True)


def main() -> int:
    args = parse_args()
    collect_root = Path(args.collect_root)
    project = Path(args.project).resolve()

    # Verify collect state exists and is active or was active
    state = read_collect_state(collect_root)
    if not state:
        print("Error: collect-state.md not found. Run '/prd-start' first.")
        return 1

    # Discover Codex home
    try:
        codex_home = find_codex_home()
    except Exception as e:
        print(f"Error: Cannot find Codex home: {e}", file=sys.stderr)
        return 1

    if not codex_home.exists():
        print(f"Error: Codex home not found: {codex_home}")
        return 1

    print(f"Codex home: {codex_home}")
    print(f"Project: {project}")

    # Determine since timestamp
    since = args.since or state.get("started_at", "")
    if since:
        print(f"Scanning sessions since: {since}")

    # Scan sessions
    if args.session_id:
        # Scan specific session
        sessions_dir = codex_home / "sessions"
        found = False
        for jsonl_path in sessions_dir.rglob("rollout-*.jsonl"):
            stem = jsonl_path.stem
            if args.session_id in stem:
                entries = parse_session_jsonl(jsonl_path)
                turns = filter_turns(entries, since=since, project_cwd=str(project))
                if turns:
                    print(f"\nSession: {args.session_id}")
                    print(f"  Found {len(turns)} turn(s)")
                    for i, (user_q, agent_a, ts) in enumerate(turns, 1):
                        print(f"  Capturing turn {i} ({ts})...")
                        capture_turn(user_q, agent_a, str(collect_root), str(project), args.agent)
                found = True
                break
        if not found:
            print(f"Session not found: {args.session_id}")
            return 1
    else:
        # Scan all project sessions
        sessions = list_project_sessions(codex_home, str(project), since=since)
        if not sessions:
            print("No Codex sessions found for this project.")
            return 0

        total_turns = 0
        captured_turns = 0
        for session in sessions:
            turns = session.get("turns", [])
            if not turns:
                continue
            thread_name = session.get("thread_name", "")
            print(f"\nSession: {session['id']}")
            print(f"  Thread: {thread_name}")
            print(f"  Turns: {len(turns)}")
            total_turns += len(turns)
            for i, (user_q, agent_a, ts) in enumerate(turns, 1):
                print(f"  Capturing turn {i} ({ts})...")
                if capture_turn(user_q, agent_a, str(collect_root), str(project), args.agent):
                    captured_turns += 1

        print(f"\nScan complete: {captured_turns}/{total_turns} turns captured.")

    # Clean up temp directory
    temp_dir = collect_root.parent / ".codex-scan-temp"
    if temp_dir.exists():
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
