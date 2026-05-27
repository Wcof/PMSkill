#!/usr/bin/env python3
"""
PRD Helper - Capture Source

Writes a conversation turn (User Query + Agent Answer) to the active capture directory.

Usage:
    python capture-source.py --user-query <text> --agent-answer <text> [--root <collect-root>] [--agent <agent-name>]
    python capture-source.py --user-query-file <path> --agent-answer-file <path> [--root <collect-root>] [--agent <agent-name>]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "_bootstrap.py").exists())))  # noqa: E501
from _bootstrap import setup_path
setup_path(__file__)

from lib.collect_writer import capture_active_turn
from lib.state import read_collect_state
from lib.constants import DEFAULT_COLLECT_ROOT


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
    # Get content
    user_query = args.user_query or ""
    agent_answer = args.agent_answer or ""
    if args.user_query_file:
        user_query = Path(args.user_query_file).read_text(encoding="utf-8")
    if args.agent_answer_file:
        agent_answer = Path(args.agent_answer_file).read_text(encoding="utf-8")

    if not user_query.strip() and not agent_answer.strip():
        print("Error: Both user query and agent answer are empty.")
        sys.exit(1)

    result = capture_active_turn(root, args.agent, user_query, agent_answer)
    if not result.written:
        print(f"Capture skipped: {result.reason}")
        sys.exit(0)

    print(f"Captured: {result.source_id}")
    print(f"File: {root / result.rel_path}")


if __name__ == "__main__":
    main()
