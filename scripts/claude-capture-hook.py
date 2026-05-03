#!/usr/bin/env python3
"""Claude Code hook for PRD Helper active capture.

UserPromptSubmit stores the user's prompt for the current session.
Stop pairs that prompt with Claude's last answer and delegates to capture-source.py.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paths import DEFAULT_COLLECT_ROOT
from lib.state import read_collect_state


SKIP_PREFIXES = (
    "/prd-helper",
    "/prd-start",
    "/prd-pause",
    "/prd-resume",
    "/prd-stop",
    "/prd-status",
    "/prd-remove",
    "/hooks",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PRD Helper Claude Code capture hook")
    parser.add_argument("--collect-root", default=DEFAULT_COLLECT_ROOT, help="Collect root directory")
    parser.add_argument("--agent", default="claude-code", help="Agent name")
    return parser.parse_args()


def read_hook_input() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def project_root(payload: dict) -> Path:
    cwd = payload.get("cwd")
    return Path(cwd).resolve() if cwd else Path.cwd().resolve()


def collect_root(project: Path, collect_root_arg: str) -> Path:
    path = Path(collect_root_arg)
    if path.is_absolute():
        return path
    return project / path


def hook_state_dir(project: Path) -> Path:
    path = project / ".claude" / "prd-helper" / "hook-state"
    path.mkdir(parents=True, exist_ok=True)
    return path


def prompt_state_file(project: Path, session_id: str) -> Path:
    safe_session = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in session_id or "unknown")
    return hook_state_dir(project) / f"{safe_session}.json"


def capture_is_on(root: Path) -> bool:
    return read_collect_state(root).get("capture_mode") == "on"


def should_skip_prompt(prompt: str) -> bool:
    stripped = prompt.strip()
    return not stripped or any(stripped.startswith(prefix) for prefix in SKIP_PREFIXES)


def handle_user_prompt(payload: dict, root: Path, project: Path) -> int:
    prompt = payload.get("prompt", "")
    if should_skip_prompt(prompt) or not capture_is_on(root):
        return 0

    session_id = payload.get("session_id", "unknown")
    state = {
        "session_id": session_id,
        "prompt": prompt,
        "transcript_path": payload.get("transcript_path", ""),
    }
    prompt_state_file(project, session_id).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


def handle_stop(payload: dict, root: Path, project: Path, agent: str) -> int:
    if not capture_is_on(root):
        return 0

    session_id = payload.get("session_id", "unknown")
    state_file = prompt_state_file(project, session_id)
    if not state_file.exists():
        return 0

    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        state_file.unlink(missing_ok=True)
        return 0

    user_query = state.get("prompt", "")
    agent_answer = payload.get("last_assistant_message", "")
    if not user_query.strip() or not agent_answer.strip():
        return 0

    temp_dir = hook_state_dir(project)
    user_file = temp_dir / f"{session_id}-user.md"
    answer_file = temp_dir / f"{session_id}-answer.md"
    user_file.write_text(user_query, encoding="utf-8")
    answer_file.write_text(agent_answer, encoding="utf-8")

    capture_script = Path(__file__).resolve().parents[1] / "modules" / "collect" / "scripts" / "capture-source.py"
    command = [
        sys.executable,
        str(capture_script),
        "--root",
        str(root),
        "--agent",
        agent,
        "--user-query-file",
        str(user_file),
        "--agent-answer-file",
        str(answer_file),
    ]
    completed = subprocess.run(command, cwd=str(project), check=False, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if completed.returncode == 0:
        state_file.unlink(missing_ok=True)
        user_file.unlink(missing_ok=True)
        answer_file.unlink(missing_ok=True)
        return 0

    if completed.stderr:
        print(completed.stderr.strip(), file=sys.stderr)
    return 1


def main() -> int:
    args = parse_args()
    payload = read_hook_input()
    project = project_root(payload)
    root = collect_root(project, args.collect_root)
    event = payload.get("hook_event_name", "")

    if event == "UserPromptSubmit":
        return handle_user_prompt(payload, root, project)
    if event == "Stop":
        return handle_stop(payload, root, project, args.agent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
