"""
采集状态文件（collect-state.md）的统一读写。

所有脚本必须通过此模块读写 collect-state.md，
不再各自实现解析逻辑。
"""

from pathlib import Path


STATE_FILE = "collect-state.md"

# 状态表格的标准 key 顺序
STATE_KEYS = (
    "capture_mode",
    "active_root",
    "passive_root",
    "session_id",
    "agent",
    "started_at",
    "paused_at",
    "resumed_at",
    "ended_at",
    "capture_scope",
    "turn_count",
    "last_collect_at",
    "last_source_id",
    "last_content_hash",
    "last_write_file",
    "total_sources",
    "active_source_count",
    "passive_source_count",
    "anomaly_count",
    "possible_noise_count",
)


def read_collect_state(root: Path) -> dict:
    """读取 collect-state.md，返回 key-value 字典。

    文件不存在时返回空 dict，不报错。
    调用方需自行判断是否需要文件必须存在。
    """
    state_file = root / STATE_FILE
    if not state_file.exists():
        return {}
    content = state_file.read_text()
    state = {}
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("|") and "|" in line[1:]:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) == 2 and cells[0] and cells[0] not in ("key", "---", ""):
                state[cells[0]] = cells[1]
    return state


def write_collect_state(root: Path, state: dict):
    """将 state 字典写入 collect-state.md。

    按 STATE_KEYS 顺序输出，未知 key 追加到末尾。
    """
    state_file = root / STATE_FILE
    lines = ["# Collect State", ""]
    lines.append("| key | value |")
    lines.append("|---|---|")
    written = set()
    for key in STATE_KEYS:
        if key in state:
            lines.append(f"| {key} | {state[key]} |")
            written.add(key)
    for key, value in state.items():
        if key not in written:
            lines.append(f"| {key} | {value} |")
    lines.append("")
    state_file.write_text("\n".join(lines))


def require_state(root: Path) -> dict:
    """读取 collect-state.md，文件不存在时退出。

    用于 capture-source.py 等必须有状态文件才能工作的脚本。
    """
    state = read_collect_state(root)
    if not state:
        import sys
        print("Error: collect-state.md not found. Run '/prd-start' first.")
        sys.exit(1)
    return state
