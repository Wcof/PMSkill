#!/usr/bin/env python3
"""Scan Codex session JSONL files and capture unrecorded conversation turns.

Usage:
    python scan-codex-sessions.py --collect-root <path> --project <path> [--agent codex] [--since <iso>] [--session-id <id>]
"""

from __future__ import annotations

import argparse
import shutil
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

from lib.codex_discovery import (
    find_codex_home,
    iter_session_files,
    list_project_sessions,
    parse_session_jsonl,
    parse_session_header,
    filter_turns,
)
from lib.state import read_collect_state
from lib.constants import DEFAULT_COLLECT_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan Codex sessions for PRD Helper capture")
    parser.add_argument("--collect-root", default=DEFAULT_COLLECT_ROOT, help="Collect root directory")
    parser.add_argument("--project", default=".", help="Project root directory")
    parser.add_argument("--agent", default="codex", help="Agent name")
    parser.add_argument("--since", default="", help="ISO timestamp to filter from")
    parser.add_argument("--session-id", default="", help="Specific session ID to scan")
    return parser.parse_args()


def capture_turn(
    user_query: str,
    agent_answer: str,
    collect_root: str,
    project: str,
    agent: str,
    capture_script: Path,
    temp_dir: Path,
    turn_index: int,
) -> bool:
    """Call capture-source.py to record a single conversation turn."""
    user_file = temp_dir / f"scan-{turn_index:04d}-user.md"
    answer_file = temp_dir / f"scan-{turn_index:04d}-answer.md"

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

    completed = subprocess.run(command, cwd=project, check=False, capture_output=True, text=True)
    if completed.returncode == 0:
        if completed.stdout:
            print(f"  {completed.stdout.strip()}")
        return True
    if completed.stderr:
        print(f"  Error: {completed.stderr.strip()}", file=sys.stderr)
    return False


def capture_session_turns(
    session_id: str,
    thread_name: str,
    turns: list[tuple[str, str, str]],
    collect_root: str,
    project: str,
    agent: str,
    capture_script: Path,
    temp_dir: Path,
    turn_offset: int = 0,
) -> tuple[int, int]:
    """Capture all turns for a session. Returns (captured, total)."""
    print(f"\nSession: {session_id}")
    if thread_name:
        print(f"  Thread: {thread_name}")
    print(f"  Turns: {len(turns)}")
    captured = 0
    for i, (user_q, agent_a, ts) in enumerate(turns, 1):
        print(f"  Capturing turn {i} ({ts})...")
        if capture_turn(user_q, agent_a, collect_root, project, agent, capture_script, temp_dir, turn_offset + i):
            captured += 1
    return captured, len(turns)


def main() -> int:
    args = parse_args()
    collect_root = Path(args.collect_root)
    project = Path(args.project).resolve()

    state = read_collect_state(collect_root)
    if not state:
        print("Error: collect-state.md not found. Run '/prd-start' first.")
        return 1

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

    since = args.since or state.get("started_at", "")
    if since:
        print(f"Scanning sessions since: {since}")

    capture_script = Path(__file__).resolve().parent / "capture-source.py"
    if not capture_script.exists():
        print(f"Error: capture script not found: {capture_script}", file=sys.stderr)
        return 1

    temp_dir = collect_root.parent / ".codex-scan-temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        if args.session_id:
            sessions_dir = codex_home / "sessions"
            found = False
            for jsonl_path, sid in iter_session_files(sessions_dir):
                if args.session_id not in sid:
                    continue
                header = parse_session_header(jsonl_path)
                meta_cwd = header.get("cwd", "")
                if str(project) and meta_cwd != str(project):
                    continue
                entries = parse_session_jsonl(jsonl_path)
                turns = filter_turns(entries, since=since)
                if turns:
                    capture_session_turns(
                        sid, "", turns, str(collect_root), str(project),
                        args.agent, capture_script, temp_dir,
                    )
                found = True
                break
            if not found:
                print(f"Session not found: {args.session_id}")
                return 1
        else:
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
                c, t = capture_session_turns(
                    session["id"],
                    session.get("thread_name", ""),
                    turns,
                    str(collect_root),
                    str(project),
                    args.agent,
                    capture_script,
                    temp_dir,
                    total_turns,
                )
                captured_turns += c
                total_turns += t

            print(f"\nScan complete: {captured_turns}/{total_turns} turns captured.")
    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
