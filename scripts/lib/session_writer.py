"""
会话文件写入 — 统一 session 文件的 frontmatter 和 turn-block 格式。

capture-source.py 和 discovery.py 都使用此模块，
避免格式漂移和字段集合不一致。
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .time_util import now_iso


def create_session_file(
    sessions_dir: Path,
    source_id: str,
    agent: str,
    session_id: str,
    turns: list[tuple[str, str]],
    extra_fields: Optional[dict[str, str]] = None,
    filename: Optional[str] = None,
) -> Path:
    """创建新的会话文件，包含 frontmatter 和所有轮次。

    Args:
        sessions_dir: 会话文件存放目录
        source_id: 来源 ID
        agent: Agent 名称
        session_id: 会话 ID
        turns: [(user_query, agent_answer), ...] 轮次列表
        extra_fields: 额外的 frontmatter 字段（如 noise_hint、content_hash）
        filename: 自定义文件名，默认 session-{session_id}.md

    Returns:
        创建的会话文件路径
    """
    sessions_dir.mkdir(parents=True, exist_ok=True)
    session_file = sessions_dir / (filename or f"session-{session_id}.md")

    ts = now_iso()
    lines = [
        "---",
        f"source_id: {source_id}",
        "source_type: agent_conversation_turn",
        "source_channel: active",
        f"source_time: {ts}",
        f"captured_at: {ts}",
        f"source_from: {agent}_conversation",
        f"agent: {agent}",
        f"session_id: {session_id}",
        f"turn_count: {len(turns)}",
        "capture_scope: full_turn",
        "status: collected",
    ]

    if extra_fields:
        for key, value in extra_fields.items():
            lines.append(f"{key}: {value}")

    lines.append("---")
    lines.append("")

    for i, (user_q, agent_a) in enumerate(turns, 1):
        lines.extend([
            f"## Turn {i}",
            "",
            "### User Query",
            "",
            user_q,
            "",
            "### Agent Answer",
            "",
            agent_a,
            "",
            "---",
            "",
        ])

    session_file.write_text("\n".join(lines), encoding="utf-8")
    return session_file


def append_turn(
    session_file: Path,
    turn_index: int,
    user_query: str,
    agent_answer: str,
) -> None:
    """向已有会话文件追加一个新轮次。"""
    turn_block = (
        f"\n---\n\n"
        f"## Turn {turn_index}\n\n"
        f"### User Query\n\n"
        f"{user_query}\n\n"
        f"### Agent Answer\n\n"
        f"{agent_answer}\n\n"
    )
    with open(session_file, "a", encoding="utf-8") as f:
        f.write(turn_block)
