#!/usr/bin/env python3
"""
PRD Helper Skill Kit - Relate Checker

Checks whether 03-relate/ satisfies the relation quality gate and writes
03-relate/check.md using the relate check template structure.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "lib").exists())))  # noqa: E501

from lib.id_registry import (
    FACT,
    QUESTION,
    CONFLICT,
    ASSUMPTION,
    PAGE,
    FEATURE,
    RULE,
    DATA,
    ACCEPTANCE,
    RELATE_ENTITIES,
    RELATION_CHAIN_RULES,
)
from lib.constants import DEFAULT_PRD_ROOT


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def check_relate(root: Path) -> dict:
    refine_dir = root / "02-refine"
    relate_dir = root / "03-relate"
    context = _read(relate_dir / "context-map.md")
    all_relate_text = "\n".join(_read(relate_dir / entity.filename) for entity in RELATE_ENTITIES)

    facts = FACT.extract_ids(_read(refine_dir / "facts.md"))
    questions = QUESTION.extract_ids(_read(refine_dir / "questions.md"))
    conflicts = CONFLICT.extract_ids(_read(refine_dir / "conflicts.md"))
    assumptions = ASSUMPTION.extract_ids(_read(refine_dir / "assumptions.md"))

    entity_ids = {
        "facts": facts,
        "pages": PAGE.extract_ids(all_relate_text),
        "features": FEATURE.extract_ids(all_relate_text),
        "rules": RULE.extract_ids(all_relate_text),
        "data": DATA.extract_ids(all_relate_text),
        "acceptance": ACCEPTANCE.extract_ids(all_relate_text),
    }

    mapped_facts = FACT.extract_ids(all_relate_text + "\n" + context)
    mapped_questions = QUESTION.extract_ids(all_relate_text + "\n" + context)
    mapped_conflicts = CONFLICT.extract_ids(all_relate_text + "\n" + context)
    mapped_assumptions = ASSUMPTION.extract_ids(all_relate_text + "\n" + context)

    return {
        "relate_exists": relate_dir.exists(),
        "context_exists": (relate_dir / "context-map.md").exists(),
        "files": {entity.filename: (relate_dir / entity.filename).exists() for entity in RELATE_ENTITIES},
        "ids": entity_ids,
        "unmapped_facts": sorted(facts - mapped_facts),
        "questions_mapped": bool(not questions or questions <= mapped_questions),
        "conflicts_mapped": bool(not conflicts or conflicts <= mapped_conflicts),
        "assumptions_mapped": bool(not assumptions or assumptions <= mapped_assumptions),
        "fact_to_page_or_feature": bool(not facts or not (facts - mapped_facts)),
        "feature_to_rule": bool(FEATURE.extract_ids(context) and RULE.extract_ids(context)),
        "rule_to_data": bool(RULE.extract_ids(context) and DATA.extract_ids(context)),
        "rule_to_acceptance": bool(RULE.extract_ids(context) and ACCEPTANCE.extract_ids(context)),
        "page_to_feature_or_rule": bool(PAGE.extract_ids(context) and (FEATURE.extract_ids(context) or RULE.extract_ids(context))),
    }


def write_check(root: Path, result: dict) -> Path:
    relate_dir = root / "03-relate"
    relate_dir.mkdir(parents=True, exist_ok=True)
    check_file = relate_dir / "check.md"

    missing_files = [fname for fname, exists in result["files"].items() if not exists]
    orphan_issues = []
    if result["unmapped_facts"]:
        orphan_issues.append("未映射事实：" + ", ".join(result["unmapped_facts"]))
    for label, ids in result["ids"].items():
        if label != "facts" and not ids:
            orphan_issues.append(f"缺少 {label} 实体")

    chain_checks = [
        (label, result[code])
        for code, label, _path in RELATION_CHAIN_RULES
    ]
    isolated_checks = [
        ("没有孤立事实", not result["unmapped_facts"]),
        ("没有孤立页面", bool(result["ids"]["pages"])),
        ("没有孤立功能", bool(result["ids"]["features"])),
        ("没有孤立规则", bool(result["ids"]["rules"])),
        ("没有孤立数据对象", bool(result["ids"]["data"])),
        ("没有孤立验收项", bool(result["ids"]["acceptance"])),
    ]
    impact_checks = [
        ("待确认问题已关联影响范围", result["questions_mapped"]),
        ("冲突点已关联影响范围", result["conflicts_mapped"]),
        ("AI 推断项已关联影响范围", result["assumptions_mapped"]),
    ]
    all_ok = result["relate_exists"] and not missing_files and all(ok for _, ok in chain_checks + isolated_checks + impact_checks)
    pending = missing_files + orphan_issues

    lines = [
        "# 关联检查",
        "",
        "## 0. 检查信息",
        "",
        "- 检查来源：check-relate.py 自动生成",
        f"- 检查状态：{'通过' if all_ok else '不通过'}",
        f"- 待确认项：{'; '.join(pending) if pending else '无'}",
        "",
        "## 1. 断链检查",
        "",
    ]
    for label, ok in chain_checks:
        lines.append(f"- [{'x' if ok else ' '}] {label}")
    lines.extend(["", "## 2. 孤立项检查", ""])
    for label, ok in isolated_checks:
        lines.append(f"- [{'x' if ok else ' '}] {label}")
    lines.extend(["", "## 3. 待确认影响检查", ""])
    for label, ok in impact_checks:
        lines.append(f"- [{'x' if ok else ' '}] {label}")
    lines.extend([
        "",
        "## 4. 关联结论",
        "",
        "本轮关联是否可以进入生成阶段：",
        "",
        f"- [{'x' if all_ok else ' '}] 可以",
        f"- [{'x' if not all_ok else ' '}] 不可以",
        f"- 原因：{'自动检查通过' if all_ok else '; '.join(pending) if pending else '存在未通过项'}",
        "",
    ])
    check_file.write_text("\n".join(lines))
    return check_file


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(DEFAULT_PRD_ROOT)
    if not root.exists():
        print(f"Error: Directory '{root}' does not exist.")
        sys.exit(1)
    result = check_relate(root)
    check_file = write_check(root, result)

    failures = []
    if not result["relate_exists"]:
        failures.append("03-relate/ missing")
    failures.extend(fname for fname, exists in result["files"].items() if not exists)
    failures.extend(result["unmapped_facts"])
    for key in ("feature_to_rule", "rule_to_data", "rule_to_acceptance", "page_to_feature_or_rule"):
        if not result[key]:
            failures.append(key)

    print("=" * 60)
    print("PRD Helper Relate Check")
    print("=" * 60)
    if failures:
        for failure in failures:
            print(f"  ❌ {failure}")
    else:
        print("  ✅ Relate checks passed")
    print(f"\nCheck written to: {check_file}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
