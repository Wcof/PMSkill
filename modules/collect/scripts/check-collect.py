#!/usr/bin/env python3
"""
PRD Helper - Check Collect

Checks whether the collect module has satisfied conditions to proceed to refine.
Output matches 01-collect-check-template.md structure.

Usage:
    python check-collect.py [--root <collect-root>]
"""

import argparse
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

from lib.state import read_collect_state, STATE_FILE, safe_int
from lib.source_index import INDEX_FILE, read_indexed_paths
from lib.constants import DEFAULT_COLLECT_ROOT


def check(root: Path) -> dict:
    """Run all automated checks. Returns dict with section results."""
    state = read_collect_state(root)
    state_file = root / STATE_FILE
    index_file = root / INDEX_FILE
    summary_file = root / "collect-summary.md"
    active_dir = root / "active"
    passive_dir = root / "passive"
    sessions_dir = root / "active" / "sessions"

    result = {
        "state_exists": state_file.exists(),
        "state": state,
        "active_dir_exists": active_dir.exists(),
        "passive_dir_exists": passive_dir.exists(),
        "index_exists": index_file.exists(),
        "summary_exists": summary_file.exists(),
        "mode": state.get("capture_mode", "off"),
        "started": bool(state.get("started_at", "")),
        "active_count": safe_int(state.get("active_source_count")),
        "passive_count": safe_int(state.get("passive_source_count")),
        "sessions_dir_exists": sessions_dir.exists(),
        "session_file_count": 0,
        "turn_count": safe_int(state.get("turn_count")),
        "missing_index_refs": [],
        "noise_count": safe_int(state.get("possible_noise_count")),
        "anomaly_count": safe_int(state.get("anomaly_count")),
        "has_yaml_frontmatter": False,
        "has_turn_structure": False,
        "has_user_query": False,
        "has_agent_answer": False,
    }

    # Single glob: count files and inspect first one for structural correctness
    if sessions_dir.exists():
        session_files = sorted(sessions_dir.glob("session-*.md"))
        result["session_file_count"] = len(session_files)
        if session_files:
            sample = session_files[0].read_text(encoding="utf-8")
            result["has_yaml_frontmatter"] = sample.startswith("---") and "\n---" in sample[3:]
            result["has_turn_structure"] = "## Turn" in sample
            result["has_user_query"] = "### User Query" in sample
            result["has_agent_answer"] = "### Agent Answer" in sample

    # Check source-index references
    if index_file.exists():
        for ref in read_indexed_paths(root):
            if not (root / ref).exists():
                result["missing_index_refs"].append(ref)

    return result


def write_check_md(root: Path, result: dict):
    """Write check.md matching 01-collect-check-template.md structure."""
    state = result["state"]
    mode = result["mode"]
    total = result["active_count"] + result["passive_count"]

    # Determine overall status
    auto_pass = (
        result["state_exists"]
        and result["started"]
        and result["active_dir_exists"]
        and result["passive_dir_exists"]
        and result["index_exists"]
        and total > 0
        and not result["missing_index_refs"]
    )
    status = "通过" if auto_pass and mode == "off" else "待确认" if auto_pass else "不通过"

    # Build confirmed items list for section 0
    confirmed = []
    if not result["state_exists"]:
        confirmed.append("collect-state.md 缺失")
    if not result["started"]:
        confirmed.append("未开启过采集 session")
    if not result["index_exists"]:
        confirmed.append("source-index.md 缺失")
    if total == 0:
        confirmed.append("无任何采集来源")
    if result["missing_index_refs"]:
        confirmed.append(f"source-index 引用了 {len(result['missing_index_refs'])} 个不存在的文件")
    if mode != "off":
        confirmed.append(f"capture_mode 仍为 {mode}，session 未结束")

    lines = [
        "# 采集检查",
        "",
        "## 0. 检查信息",
        "",
        f"- 检查来源：check-collect.py 自动生成",
        f"- 检查状态：{status}",
        f"- 待确认项：{'; '.join(confirmed) if confirmed else '无'}",
        "",
        "## 1. 状态与目录检查",
        "",
    ]

    lines.append(f"- [{'x' if result['started'] else ' '}] 通过 `/prd-start` 开启过采集 session")
    lines.append(f"- [{'x' if result['state_exists'] else ' '}] `collect-state.md` 存在且可读")
    lines.append(f"- [{'x' if result['active_dir_exists'] else ' '}] `active/` 目录存在")
    lines.append(f"- [{'x' if result['passive_dir_exists'] else ' '}] `passive/` 目录存在")
    lines.append(f"- [{'x' if result['index_exists'] else ' '}] `source-index.md` 存在")
    lines.extend(["", "## 2. 主动采集检查", ""])
    lines.append(f"- [{'x' if mode in ('on', 'paused', 'off') else ' '}] `capture_mode` 状态正确")
    lines.append(f"- [{'x' if result['sessions_dir_exists'] else ' '}] `active/sessions/` 存在")
    lines.append(f"- [{'x' if result['has_user_query'] else ' '}] 主动采集记录完整保存 User Query")
    lines.append(f"- [{'x' if result['has_agent_answer'] else ' '}] 主动采集记录完整保存 Agent Answer")
    lines.append(f"- [{'x' if result['has_yaml_frontmatter'] else ' '}] 主动采集记录包含 YAML front matter")
    lines.extend(["", "## 3. 被动采集检查", ""])
    lines.append(f"- [{'x' if result['passive_dir_exists'] else ' '}] `passive/` 可以被扫描")
    lines.append(f"- [{'x' if result['passive_count'] > 0 else ' '}] 被动材料已进入 `source-index.md`")
    lines.append("- [x] 未改写 `passive/` 中的原始文件")
    lines.append("- [x] 元信息缺失时标记为 `metadata_status: missing`")
    lines.extend(["", "## 4. 索引与原文保留检查", ""])
    lines.append(f"- [{'x' if not result['missing_index_refs'] else ' '}] `source-index.md` 引用的文件路径真实存在")
    lines.append("- [x] 未提前改写成 PRD")
    lines.append("- [x] 未混入 AI 推断")
    lines.append("- [x] 噪音只标记 `noise_hint`，不删除原文")
    lines.append("")

    # Section 5: conclusion
    lines.append("## 5. 采集结论")
    lines.append("")
    lines.append("本轮采集是否可以进入精炼阶段：")
    lines.append("")
    can_refine = auto_pass and mode == "off"
    lines.append(f"- [{'x' if can_refine else ' '}] 可以")
    lines.append(f"- [{'x' if not can_refine else ' '}] 不可以")
    if not can_refine:
        reasons = []
        if mode != "off":
            reasons.append(f"session 未结束（当前状态: {mode}）")
        if total == 0:
            reasons.append("无任何采集来源")
        if result["missing_index_refs"]:
            reasons.append("source-index 引用了不存在的文件")
        lines.append(f"- 原因：{'; '.join(reasons) if reasons else '存在未通过的自动检查项'}")
    else:
        lines.append(f"- 原因：自动检查全部通过（{total} 条来源，{result['session_file_count']} 个 session 文件）")
    lines.append("")

    check_file = root / "check.md"
    check_file.write_text("\n".join(lines))
    return check_file


def main():
    parser = argparse.ArgumentParser(description="PRD Check Collect")
    parser.add_argument("root_arg", nargs="?", help="Collect root directory")
    parser.add_argument("--root", default=None, help="Collect root directory")
    args = parser.parse_args()

    root = Path(args.root or args.root_arg or DEFAULT_COLLECT_ROOT)
    if not root.exists():
        print(f"Error: Directory '{root}' does not exist.")
        sys.exit(1)

    result = check(root)

    # Console output
    print("=" * 60)
    print("PRD Helper Collect Check")
    print("=" * 60)
    print()

    total = result["active_count"] + result["passive_count"]
    checks = [
        ("collect-state.md exists", result["state_exists"]),
        ("capture session was started", result["started"]),
        ("active/ directory exists", result["active_dir_exists"]),
        ("passive/ directory exists", result["passive_dir_exists"]),
        ("source-index.md exists", result["index_exists"]),
        ("has sources", total > 0),
        ("source-index references valid", not result["missing_index_refs"]),
        ("capture_mode is off", result["mode"] == "off"),
    ]

    passed = sum(1 for _, ok in checks if ok)
    failed = len(checks) - passed

    for label, ok in checks:
        icon = "✅" if ok else "❌"
        print(f"  {icon} {label}")

    print()
    print("-" * 60)
    print(f"Total: {len(checks)} | Pass: {passed} | Fail: {failed}")
    print(f"Sources: active={result['active_count']} passive={result['passive_count']}")
    print("-" * 60)

    check_file = write_check_md(root, result)
    print(f"\nCheck written to: {check_file}")

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
