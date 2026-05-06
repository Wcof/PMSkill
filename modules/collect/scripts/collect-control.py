#!/usr/bin/env python3
"""
PRD Helper - Collect Control

Controls PRD Capture Session: start, pause, resume, stop, status, scan.

Usage:
    python collect-control.py <command> [--root <collect-root>] [--agent <agent-name>]

Commands:
    start   - Start a new PRD Capture Session
    pause   - Pause the current session
    resume  - Resume the current session
    stop    - Stop the current session, generate summary and check
    status  - Show current capture state
    scan    - Scan all AI tool sessions for the current project
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "lib").exists())))  # noqa: E501

from lib.state import read_collect_state, write_collect_state, default_state, transition, InvalidTransition
from lib.time_util import now_iso, now_id
from lib.source_index import ensure_index
from lib.constants import DEFAULT_COLLECT_ROOT, DEFAULT_PRD_ROOT
from lib.claude_hooks import install_claude_hooks, remove_claude_hooks
from lib.template_path import module_template_path
from lib.template_renderer import render_template


def ensure_dirs(root: Path):
    """Ensure active/ and passive/ directories exist."""
    (root / "active" / "sessions").mkdir(parents=True, exist_ok=True)
    (root / "active" / "historical").mkdir(parents=True, exist_ok=True)
    (root / "active" / "anomalies").mkdir(parents=True, exist_ok=True)
    (root / "passive").mkdir(parents=True, exist_ok=True)


def sync_claude_hooks(project: Path, docs_root: str, agent: str, enabled: bool) -> None:
    """Install or remove Claude Code hooks to match capture mode."""
    if agent != "claude-code":
        return
    if enabled:
        hook_file = install_claude_hooks(project, docs_root)
        print(f"Claude Code hooks enabled: {hook_file}")
    else:
        hook_file = remove_claude_hooks(project)
        if hook_file:
            print(f"Claude Code hooks removed: {hook_file}")
        else:
            print("Claude Code hooks already clean.")


def cmd_start(root: Path, agent: str, project: Path, docs_root: str):
    """Start a new PRD Capture Session."""
    ensure_dirs(root)

    state = read_collect_state(root)
    current_mode = state.get("capture_mode", "off")

    # 已经在采集中，只同步 hooks
    if current_mode == "on":
        sync_claude_hooks(project, docs_root, agent, True)
        print(f"Already capturing (session: {state.get('session_id', 'unknown')})")
        if agent == "claude-code":
            print("Claude Code hooks verified.")
        print("Use '/prd-stop' to stop first.")
        return

    # 验证状态转换
    try:
        transition(current_mode, "on")
    except InvalidTransition as e:
        print(f"Cannot start: {e}")
        return

    # 复用已有 session（stop 后再 start）
    existing_session_id = state.get("session_id", "")
    if existing_session_id:
        state["capture_mode"] = "on"
        state["agent"] = agent
        state["resumed_at"] = now_iso()
        state["ended_at"] = ""
        write_collect_state(root, state)
        sync_claude_hooks(project, docs_root, agent, True)
        print(f"PRD Capture Session resumed: {existing_session_id}")
        print(f"Agent: {agent}")
        print(f"Capture mode: on")
        return

    session_id = f"prd-session-{now_id()}"

    new_state = default_state()
    new_state.update({
        "capture_mode": "on",
        "active_root": str(root / "active"),
        "passive_root": str(root / "passive"),
        "session_id": session_id,
        "agent": agent,
        "started_at": now_iso(),
        "capture_scope": "full_turn",
        "total_sources": state.get("total_sources", "0"),
        "passive_source_count": state.get("passive_source_count", "0"),
        "grill_mode": "off",
    })

    write_collect_state(root, new_state)
    ensure_index(root)
    sync_claude_hooks(project, docs_root, agent, True)

    print(f"PRD Capture Session started: {session_id}")
    print(f"Agent: {agent}")
    print(f"Active root: {root / 'active'}")
    print(f"Passive root: {root / 'passive'}")
    print(f"Capture mode: on")


def _run_scan(root: Path, project: Path, agent: str) -> int:
    """Run scan-all-sessions.py and return its exit code."""
    scan_script = Path(__file__).resolve().parent / "scan-all-sessions.py"
    if not scan_script.exists():
        print(f"Session scanner not found: {scan_script}")
        return 1
    cmd = [
        sys.executable,
        str(scan_script),
        "--collect-root",
        str(root),
        "--project",
        str(project),
        "--agent",
        agent,
    ]
    return subprocess.run(cmd, cwd=str(project), check=False).returncode


def cmd_stop(root: Path, agent: str, project: Path):
    """Stop the current PRD Capture Session."""
    state = read_collect_state(root)
    current_mode = state.get("capture_mode", "off")

    try:
        transition(current_mode, "off")
    except InvalidTransition as e:
        print(f"Cannot stop: {e}")
        return

    # Scan all AI tool sessions before stopping
    _run_scan(root, project, agent)

    state["capture_mode"] = "off"
    state["grill_mode"] = "off"
    state["ended_at"] = now_iso()
    write_collect_state(root, state)
    sync_claude_hooks(project, "", agent, False)

    summary_file = root / "collect-summary.md"
    summary_values = {
        key: state.get(key, "0")
        for key in (
            "turn_count",
            "active_source_count",
            "passive_source_count",
            "anomaly_count",
            "possible_noise_count",
        )
    }
    summary_values.update({
        key: state.get(key, "")
        for key in ("session_id", "agent", "started_at", "ended_at")
    })
    summary = render_template(module_template_path(__file__, "collect-summary-template.md"), summary_values)
    summary_file.write_text(summary, encoding="utf-8")

    print(f"Session stopped: {state.get('session_id')}")
    print(f"Summary written to: {summary_file}")
    print("可以用 `/prd-refine` 开始精炼。")


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


def cmd_scan(root: Path, project: Path, agent: str):
    """Scan all AI tool sessions for the current project."""
    return _run_scan(root, project, agent)


def main():
    parser = argparse.ArgumentParser(description="PRD Collect Control")
    parser.add_argument("command", choices=["start", "stop", "status", "scan"])
    parser.add_argument("--root", default=DEFAULT_COLLECT_ROOT, help="Collect root directory")
    parser.add_argument("--project", default=".", help="Project root directory")
    parser.add_argument("--docs-root", default=DEFAULT_PRD_ROOT, help="PRD Helper docs root directory")
    parser.add_argument("--agent", default="unknown", help="Agent name")

    args = parser.parse_args()
    root = Path(args.root)
    project = Path(args.project).resolve()

    commands = {
        "start": lambda: cmd_start(root, args.agent, project, args.docs_root),
        "stop": lambda: cmd_stop(root, args.agent, project),
        "status": lambda: cmd_status(root),
        "scan": lambda: cmd_scan(root, project, args.agent),
    }

    commands[args.command]()


if __name__ == "__main__":
    main()
