#!/usr/bin/env python3
"""
PRD Helper - Capture Source

Writes a conversation turn (User Query + Agent Answer) to the active capture directory.

Usage:
    python capture-source.py --user-query <text> --agent-answer <text> [--root <collect-root>] [--agent <agent-name>]
    python capture-source.py --user-query-file <path> --agent-answer-file <path> [--root <collect-root>] [--agent <agent-name>]
"""

import argparse
import re
import sys
from pathlib import Path

# Add scripts/ to path for lib imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.state import read_collect_state, write_collect_state
from lib.time_util import now_iso, now_id
from lib.hash_util import content_hash
from lib.source_index import append_index
from lib.paths import DEFAULT_COLLECT_ROOT


def detect_noise(user_query: str, agent_answer: str) -> tuple[str, str]:
    """Lightweight noise detection."""
    combined = user_query.strip()
    noise_patterns = [
        (r"^(好的|嗯嗯|继续|ok|okay|yes|是的|对的|知道了)\s*[。.!?！？]*$", "possible_noise"),
        (r"^\s*$", "possible_noise"),
    ]
    for pattern, hint in noise_patterns:
        if re.match(pattern, combined, re.IGNORECASE):
            return hint, "短回复或空内容，可能是噪音"
    return "none", ""


def main():
    parser = argparse.ArgumentParser(description="PRD Capture Source")
    parser.add_argument("--user-query", help="User query text")
    parser.add_argument("--agent-answer", help="Agent answer text")
    parser.add_argument("--user-query-file", help="Path to user query file")
    parser.add_argument("--agent-answer-file", help="Path to agent answer file")
    parser.add_argument("--root", default=DEFAULT_COLLECT_ROOT, help="Collect root directory")
    parser.add_argument("--agent", default="unknown", help="Agent name")

    args = parser.parse_args()
    root = Path(args.root)

    # Read state
    state = read_collect_state(root)
    if not state:
        print("Error: collect-state.md not found. Run '/prd-start' first.")
        sys.exit(1)
    if state.get("capture_mode") != "on":
        print(f"Capture mode is '{state.get('capture_mode', 'off')}', not writing.")
        sys.exit(0)

    # Get content
    user_query = args.user_query or ""
    agent_answer = args.agent_answer or ""
    if args.user_query_file:
        user_query = Path(args.user_query_file).read_text()
    if args.agent_answer_file:
        agent_answer = Path(args.agent_answer_file).read_text()

    if not user_query.strip() and not agent_answer.strip():
        print("Error: Both user query and agent answer are empty.")
        sys.exit(1)

    # Generate IDs
    ts = now_id()
    session_id = state.get("session_id", "unknown")
    turn_index = str(int(state.get("turn_count", "0")) + 1)
    source_id = f"turn-{ts}-{turn_index.zfill(3)}"

    # Compute hash
    combined = user_query + agent_answer
    c_hash = content_hash(combined)

    # Detect noise
    noise_hint, noise_reason = detect_noise(user_query, agent_answer)

    # Write session file
    sessions_dir = root / "active" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    session_file = sessions_dir / f"{source_id}.md"

    content = f"""---
source_id: {source_id}
source_type: agent_conversation_turn
source_channel: active
source_time: {now_iso()}
captured_at: {now_iso()}
source_from: {args.agent}_conversation
agent: {args.agent}
session_id: {session_id}
turn_index: {turn_index}
capture_scope: full_turn
content_hash: {c_hash}
noise_hint: {noise_hint}
noise_reason: {noise_reason}
status: collected
---

## User Query

{user_query}

## Agent Answer

{agent_answer}

## Capture Note

本轮为完整会话采集，未做事实提取、需求判断或清洗。
"""
    session_file.write_text(content)

    # Update state
    state["turn_count"] = turn_index
    state["last_collect_at"] = now_iso()
    state["last_source_id"] = source_id
    state["last_content_hash"] = c_hash
    state["last_write_file"] = str(session_file)
    state["active_source_count"] = str(int(state.get("active_source_count", "0")) + 1)
    state["total_sources"] = str(int(state.get("total_sources", "0")) + 1)
    if noise_hint == "possible_noise":
        state["possible_noise_count"] = str(int(state.get("possible_noise_count", "0")) + 1)
    write_collect_state(root, state)

    # Update source index
    append_index(root, {
        "source_id": source_id,
        "source_time": now_iso(),
        "source_type": "agent_conversation_turn",
        "source_channel": "active",
        "path": str(session_file.relative_to(root)),
        "content_hash": c_hash,
        "metadata_status": "complete",
        "noise_hint": noise_hint,
        "status": "collected",
    })

    print(f"Captured: {source_id} (turn {turn_index})")
    print(f"File: {session_file}")


if __name__ == "__main__":
    main()
