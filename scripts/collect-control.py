#!/usr/bin/env python3
"""
PRD Helper - Collect Control

Controls PRD Capture Session: start, pause, resume, stop, status.

Usage:
    python collect-control.py <command> [--root <collect-root>] [--agent <agent-name>]

Commands:
    start   - Start a new PRD Capture Session
    pause   - Pause the current session
    resume  - Resume the current session
    stop    - Stop the current session, generate summary and check
    status  - Show current capture state
"""

import argparse
import sys
from pathlib import Path

# Add scripts/ to path for lib imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.state import read_collect_state, write_collect_state
from lib.time_util import now_iso, now_id
from lib.source_index import ensure_index
from lib.paths import DEFAULT_COLLECT_ROOT


def ensure_dirs(root: Path):
    """Ensure active/ and passive/ directories exist."""
    (root / "active" / "sessions").mkdir(parents=True, exist_ok=True)
    (root / "active" / "historical").mkdir(parents=True, exist_ok=True)
    (root / "active" / "anomalies").mkdir(parents=True, exist_ok=True)
    (root / "passive").mkdir(parents=True, exist_ok=True)


def cmd_start(root: Path, agent: str):
    """Start a new PRD Capture Session."""
    ensure_dirs(root)

    state = read_collect_state(root)
    if state.get("capture_mode") == "on":
        print(f"Already capturing (session: {state.get('session_id', 'unknown')})")
        print("Use '/prd-pause' to pause or '/prd-stop' to stop first.")
        return

    session_id = f"prd-session-{now_id()}"

    new_state = {
        "capture_mode": "on",
        "active_root": str(root / "active"),
        "passive_root": str(root / "passive"),
        "session_id": session_id,
        "agent": agent,
        "started_at": now_iso(),
        "paused_at": "",
        "resumed_at": "",
        "ended_at": "",
        "capture_scope": "full_turn",
        "turn_count": "0",
        "last_collect_at": "",
        "last_source_id": "",
        "last_content_hash": "",
        "last_write_file": "",
        "total_sources": state.get("total_sources", "0"),
        "active_source_count": "0",
        "passive_source_count": state.get("passive_source_count", "0"),
        "anomaly_count": "0",
        "possible_noise_count": "0",
    }

    write_collect_state(root, new_state)
    ensure_index(root)

    print(f"PRD Capture Session started: {session_id}")
    print(f"Agent: {agent}")
    print(f"Active root: {root / 'active'}")
    print(f"Passive root: {root / 'passive'}")
    print(f"Capture mode: on")


def cmd_pause(root: Path):
    """Pause the current PRD Capture Session."""
    state = read_collect_state(root)
    if state.get("capture_mode") != "on":
        print(f"Cannot pause: current mode is '{state.get('capture_mode', 'off')}'")
        return

    state["capture_mode"] = "paused"
    state["paused_at"] = now_iso()
    write_collect_state(root, state)
    print(f"Session paused: {state.get('session_id')}")


def cmd_resume(root: Path):
    """Resume the current PRD Capture Session."""
    state = read_collect_state(root)
    if state.get("capture_mode") != "paused":
        print(f"Cannot resume: current mode is '{state.get('capture_mode', 'off')}'")
        return

    state["capture_mode"] = "on"
    state["resumed_at"] = now_iso()
    write_collect_state(root, state)
    print(f"Session resumed: {state.get('session_id')}")


def cmd_stop(root: Path):
    """Stop the current PRD Capture Session."""
    state = read_collect_state(root)
    if state.get("capture_mode") not in ("on", "paused"):
        print(f"Cannot stop: current mode is '{state.get('capture_mode', 'off')}'")
        return

    state["capture_mode"] = "off"
    state["ended_at"] = now_iso()
    write_collect_state(root, state)

    # Generate collect-summary.md
    summary_file = root / "collect-summary.md"
    summary_lines = [
        "# Collect Summary",
        "",
        f"- Session: {state.get('session_id', '')}",
        f"- Agent: {state.get('agent', '')}",
        f"- Started: {state.get('started_at', '')}",
        f"- Ended: {state.get('ended_at', '')}",
        f"- Total turns: {state.get('turn_count', '0')}",
        f"- Active sources: {state.get('active_source_count', '0')}",
        f"- Passive sources: {state.get('passive_source_count', '0')}",
        f"- Anomalies: {state.get('anomaly_count', '0')}",
        f"- Possible noise: {state.get('possible_noise_count', '0')}",
        "",
    ]
    summary_file.write_text("\n".join(summary_lines))

    print(f"Session stopped: {state.get('session_id')}")
    print(f"Summary written to: {summary_file}")
    print("Run 'check-collect.py' to verify collect is ready for refine.")


def cmd_status(root: Path):
    """Show current capture state."""
    state = read_collect_state(root)
    if not state:
        print("No collect state found. Run '/prd-start' first.")
        return

    print("=" * 50)
    print("PRD Capture Status")
    print("=" * 50)
    for key, value in state.items():
        print(f"  {key}: {value}")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="PRD Collect Control")
    parser.add_argument("command", choices=["start", "pause", "resume", "stop", "status"])
    parser.add_argument("--root", default=DEFAULT_COLLECT_ROOT, help="Collect root directory")
    parser.add_argument("--agent", default="unknown", help="Agent name")

    args = parser.parse_args()
    root = Path(args.root)

    commands = {
        "start": lambda: cmd_start(root, args.agent),
        "pause": lambda: cmd_pause(root),
        "resume": lambda: cmd_resume(root),
        "stop": lambda: cmd_stop(root),
        "status": lambda: cmd_status(root),
    }

    commands[args.command]()


if __name__ == "__main__":
    main()
