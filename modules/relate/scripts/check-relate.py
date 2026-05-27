#!/usr/bin/env python3
"""
PRD Helper Skill Kit - Relate Checker

Checks whether 03-relate/ satisfies the relation quality gate and writes
03-relate/check.md using the relate check template structure.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "_bootstrap.py").exists())))  # noqa: E501
from _bootstrap import setup_path
setup_path(__file__)

from lib.id_registry import RELATE_ENTITIES, RELATION_CHAIN_RULES, get_entity
from lib.constants import DEFAULT_PRD_ROOT
from lib.check_framework import CheckWriter, print_header, print_footer
from lib.template_path import module_template_path
from lib.relation_chain import parse_relation_chain, relation_chain_report


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def check_relate(root: Path) -> dict:
    refine_dir = root / "02-refine"
    relate_dir = root / "03-relate"
    context = _read(relate_dir / "context-map.md")
    chain_report = relation_chain_report(parse_relation_chain(root))

    fact = get_entity("fact")
    question = get_entity("question")
    conflict = get_entity("conflict")
    assumption = get_entity("assumption")
    all_relate_text = "\n".join(_read(relate_dir / entity.filename) for entity in RELATE_ENTITIES)

    facts = fact.extract_ids(_read(refine_dir / "facts.md"))
    questions = question.extract_ids(_read(refine_dir / "questions.md"))
    conflicts = conflict.extract_ids(_read(refine_dir / "conflicts.md"))
    assumptions = assumption.extract_ids(_read(refine_dir / "assumptions.md"))

    entity_ids = {
        "facts": facts,
        "pages": chain_report["entities"]["page"],
        "features": chain_report["entities"]["feature"],
        "rules": chain_report["entities"]["rule"],
        "data": chain_report["entities"]["data"],
        "acceptance": chain_report["entities"]["acceptance"],
    }

    mapped_facts = fact.extract_ids(context)
    mapped_questions = question.extract_ids(all_relate_text + "\n" + context)
    mapped_conflicts = conflict.extract_ids(all_relate_text + "\n" + context)
    mapped_assumptions = assumption.extract_ids(all_relate_text + "\n" + context)

    return {
        "relate_exists": relate_dir.exists(),
        "context_exists": (relate_dir / "context-map.md").exists(),
        "files": {entity.filename: (relate_dir / entity.filename).exists() for entity in RELATE_ENTITIES},
        "ids": entity_ids,
        "unmapped_facts": sorted(facts - mapped_facts),
        "questions_mapped": bool(not questions or questions <= mapped_questions),
        "conflicts_mapped": bool(not conflicts or conflicts <= mapped_conflicts),
        "assumptions_mapped": bool(not assumptions or assumptions <= mapped_assumptions),
        "fact_to_page_or_feature": chain_report["rule_checks"]["fact_to_page_or_feature"],
        "feature_to_rule": chain_report["rule_checks"]["feature_to_rule"],
        "rule_to_data": chain_report["rule_checks"]["rule_to_data"],
        "rule_to_acceptance": chain_report["rule_checks"]["rule_to_acceptance"],
        "page_to_feature_or_rule": chain_report["rule_checks"]["page_to_feature_or_rule"],
        "relation_chain": chain_report,
    }


def write_check(root: Path, result: dict) -> Path:
    relate_dir = root / "03-relate"
    relate_dir.mkdir(parents=True, exist_ok=True)

    missing_files = [fname for fname, exists in result["files"].items() if not exists]
    orphan_issues = []
    if result["unmapped_facts"]:
        orphan_issues.append("未映射事实：" + ", ".join(result["unmapped_facts"]))
    for break_item in result.get("relation_chain", {}).get("breaks", []):
        orphan_issues.append(f"{break_item['fact_id']} 缺少 {break_item['missing']} 链路")
    for label, ids in result["ids"].items():
        if label != "facts" and not ids:
            orphan_issues.append(f"缺少 {label} 实体")

    chain_checks = [
        (result[code], label)
        for code, label, _path in RELATION_CHAIN_RULES
    ]
    isolated_checks = [
        (not result["unmapped_facts"], "没有孤立事实"),
        (bool(result["ids"]["pages"]), "没有孤立页面"),
        (bool(result["ids"]["features"]), "没有孤立功能"),
        (bool(result["ids"]["rules"]), "没有孤立规则"),
        (bool(result["ids"]["data"]), "没有孤立数据对象"),
        (bool(result["ids"]["acceptance"]), "没有孤立验收项"),
    ]
    impact_checks = [
        (result["questions_mapped"], "待确认问题已关联影响范围"),
        (result["conflicts_mapped"], "冲突点已关联影响范围"),
        (result["assumptions_mapped"], "AI 推断项已关联影响范围"),
    ]
    all_ok = result["relate_exists"] and not missing_files and all(ok for ok, _ in chain_checks + isolated_checks + impact_checks)
    pending = missing_files + orphan_issues

    w = CheckWriter(relate_dir, template_path=module_template_path(__file__, "03-relate-check-template.md"))
    w.add_meta("检查来源", "check-relate.py 自动生成")
    w.add_meta("检查状态", "通过" if all_ok else "不通过")
    w.add_meta("待确认项", "; ".join(pending) if pending else "无")

    w.add_template_section("1. 断链检查", {label: ok for ok, label in chain_checks})
    w.add_template_section("2. 孤立项检查", {label: ok for ok, label in isolated_checks})
    w.add_template_section("3. 待确认影响检查", {label: ok for ok, label in impact_checks})

    w.add_conclusion(
        can_proceed=all_ok,
        reason="自动检查通过" if all_ok else "; ".join(pending) if pending else "存在未通过项",
    )
    return w.write()


def main() -> None:
    parser = argparse.ArgumentParser(description="PRD Check Relate")
    parser.add_argument("root_arg", nargs="?", help="PRD root directory")
    parser.add_argument("--root", default=None, help="PRD root directory")
    args = parser.parse_args()

    root = Path(args.root or args.root_arg or DEFAULT_PRD_ROOT)
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
    failures.extend(f"{item['fact_id']} 缺少 {item['missing']} 链路" for item in result["relation_chain"]["breaks"])
    for key in ("feature_to_rule", "rule_to_data", "rule_to_acceptance", "page_to_feature_or_rule"):
        if not result[key]:
            failures.append(key)

    print_header("PRD Helper Relate Check")
    if failures:
        for failure in failures:
            print(f"  ❌ {failure}")
    else:
        print("  ✅ Relate checks passed")
    print(f"\nCheck written to: {check_file}")
    # 报告模式：无数据时不阻断，有数据时检查错误
    if not result["relate_exists"]:
        sys.exit(0)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
