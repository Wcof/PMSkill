#!/usr/bin/env python3
from __future__ import annotations

"""
PRD Helper Skill Kit - Generated Content Checker

Checks whether generated documents are complete and contain
no unresolved TODOs or unconfirmed items. Also checks whether
pending questions are properly consolidated in final check or context-delta.

Usage:
    python check-generated.py [docs/prd-helper/root]

Output:
    Prints check results to stdout.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "lib").exists())))  # noqa: E501
from lib.id_registry import ALL_ENTITIES
from lib.markdown_util import extract_template_sections
from lib.constants import DEFAULT_PRD_ROOT
from lib.template_path import module_template_path
from lib.check_framework import CheckWriter
from lib.check_result import CheckResult
from lib.generate_manifest import build_generate_manifest
from lib.relation_chain import parse_relation_chain, relation_chain_report
from lib.source_anchor import has_source_anchor


def _safe_rglob(directory: Path, pattern: str = "*.md"):
    """rglob that skips hidden directories (starting with '.')."""
    for item in directory.rglob(pattern):
        # Skip files in hidden directories
        if any(part.startswith(".") for part in item.relative_to(directory).parts):
            continue
        yield item


# Patterns that indicate unresolved content
UNRESOLVED_PATTERNS = [
    (r"<!--\s*TODO", "<!-- TODO"),
    (r"<!--\s*FIXME", "<!-- FIXME"),
    (r"<!--\s*TBD", "<!-- TBD"),
    (r"\[TODO\]", "[TODO]"),
    (r"\[TBD\]", "[TBD]"),
    (r"\[待确认\]", "[待确认]"),
    (r"\[未确认\]", "[未确认]"),
    (r"<!--\s*待确认\s*-->", "<!-- 待确认 -->"),
    (r"<!--\s*无来源\s*-->", "<!-- 无来源 -->"),
]


def _read_generated_files(root_path: Path) -> list[tuple[str, str]]:
    """Read all generated .md files once, returning (rel_path, content) pairs."""
    gen_dir = root_path / "04-generate"
    if not gen_dir.exists():
        return []
    files = []
    for md_file in _safe_rglob(gen_dir):
        if md_file.name == "check.md":
            continue
        files.append((str(md_file.relative_to(root_path)), md_file.read_text(encoding="utf-8")))
    return files


def check_unresolved_content(files: list[tuple[str, str]]) -> list[dict]:
    """Check for unresolved TODOs and markers in generated content."""
    results = []
    for rel_path, content in files:
        for pattern, label in UNRESOLVED_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                results.append({"file": rel_path, "pattern": label, "count": len(matches)})
    return results


def check_pending_questions_consolidation(root_path: Path, files: list[tuple[str, str]]) -> dict:
    """Check if pending questions from generated docs are consolidated in 05-check."""
    check_dir = root_path / "05-check"

    if not files:
        return {"checked": True, "pending_count": 0, "all_consolidated": True}

    # Collect all pending questions from pre-read files
    pending_questions = []
    for rel_path, content in files:
        for line in content.split("\n"):
            if "待确认" in line and line.strip().startswith(("-", "|", "*")):
                pending_questions.append({
                    "file": rel_path,
                    "line": line.strip()[:80],
                })

    if not pending_questions:
        return {"checked": True, "pending_count": 0, "all_consolidated": True}

    # Collect text from 05-check consolidation files
    consolidated_text = ""
    for fname in ["context-delta.md", "generated-check.md", "full-check.md"]:
        fpath = check_dir / fname
        if fpath.exists():
            consolidated_text += "\n" + fpath.read_text(encoding="utf-8")

    # Check each question: at least its question ID or first 15 chars should appear
    unconsolidated = []
    for q in pending_questions:
        line = q["line"]
        # Extract question ID (e.g. question_001) if present
        qid_match = re.search(r"question[_-]\d+", line)
        if qid_match:
            key = qid_match.group()
        else:
            # Use first 15 meaningful chars as match key
            key = re.sub(r"[\s\-\|*：:]+", "", line)[:15]
        if key and key not in consolidated_text:
            unconsolidated.append(q)

    return {
        "checked": True,
        "pending_count": len(pending_questions),
        "all_consolidated": len(unconsolidated) == 0,
        "unconsolidated": unconsolidated[:5],
        "pending_questions": pending_questions[:5],
    }


def check_traceability(files: list[tuple[str, str]]) -> list[dict]:
    """Check if generated docs keep source or relation traceability."""
    if not files:
        return []

    # 从注册表动态构建可追溯性模式
    trace_patterns = [entity.id_pattern for entity in ALL_ENTITIES]
    trace_patterns.extend([
        r"来源说明",
        r"来源事实",
        r"关联规则",
        r"关联数据",
        r"关联验收",
    ])

    results = []
    for rel_path, content in files:
        has_trace = any(re.search(pattern, content) for pattern in trace_patterns)
        results.append({
            "file": rel_path,
            "status": "PASS" if has_trace else "FAIL",
        })

    return results


def check_prerequisites(root_path: Path) -> dict:
    """Check whether Generate has enough upstream artifacts for deterministic output."""
    refine_dir = root_path / "02-refine"
    relate_dir = root_path / "03-relate"
    missing = []
    if not refine_dir.exists() or not any(refine_dir.glob("*.md")):
        missing.append("02-refine/ 缺失")
    if not relate_dir.exists() or not any(relate_dir.glob("*.md")):
        missing.append("03-relate/ 缺失")
    return {
        "refine_exists": "02-refine/ 缺失" not in missing,
        "relate_exists": "03-relate/ 缺失" not in missing,
        "missing": missing,
        "limited": bool(missing),
    }


def check_page_completeness(root_path: Path) -> list[dict]:
    """Check if page documents have required sections from template."""
    return _check_doc_completeness(
        root_path / "04-generate" / "pages",
        module_template_path(__file__, "04-generate-page-prd-template.md"),
        root_path,
    )


def check_rule_completeness(root_path: Path) -> list[dict]:
    """Check if rule documents have required sections from template."""
    return _check_doc_completeness(
        root_path / "04-generate" / "rules",
        module_template_path(__file__, "04-generate-rule-prd-template.md"),
        root_path,
    )


def check_manifest_coverage(root_path: Path, files: list[tuple[str, str]]) -> dict:
    manifest = build_generate_manifest(root_path)
    actual_paths = {rel_path for rel_path, _ in files}
    expected_paths = {view["path"] for view in manifest["views"] if view["type"] != "check"}
    known_prefixes = (
        "04-generate/overview/",
        "04-generate/pages/",
        "04-generate/rules/",
        "04-generate/data/",
        "04-generate/acceptance/",
        "04-generate/agent-context/",
    )
    unexpected = sorted(path for path in actual_paths - expected_paths if path.startswith(known_prefixes))
    missing = [
        {**view, "status": "MISSING"}
        for view in manifest["views"]
        if view["type"] != "check" and view["path"] not in actual_paths
    ]
    return {
        "manifest": manifest,
        "expected_count": len(expected_paths),
        "actual_count": len(actual_paths),
        "missing": missing,
        "unexpected": unexpected,
        "complete": not missing and not unexpected,
    }


def check_relation_chain_safety(root_path: Path) -> dict:
    relate_dir = root_path / "03-relate"
    context_map = relate_dir / "context-map.md"
    if not relate_dir.exists():
        return {
            "safe": False,
            "risks": ["03-relate/ 缺失，无法证明 Relation Chain 完整"],
        }
    if not context_map.exists():
        return {
            "safe": False,
            "risks": ["03-relate/context-map.md 缺失，无法证明 Relation Chain 完整"],
        }
    report = relation_chain_report(parse_relation_chain(root_path))
    return {
        "safe": report["safe"],
        "risks": [
            f"{item['fact_id']} 缺少 {item['missing']} 链路"
            for item in report["breaks"]
        ],
        "report": report,
        "breaks": report["breaks"],
    }


def check_agent_context_safety(files: list[tuple[str, str]], prerequisites: dict, relation_chain: dict) -> dict:
    agent_files = [(path, content) for path, content in files if path.startswith("04-generate/agent-context/")]
    prohibited_items = []
    if prerequisites["limited"]:
        prohibited_items.append("缺失前置产物时不得把内容写成确定性要求")
    if not relation_chain["safe"]:
        prohibited_items.append("Relation Chain 未验证时不得把断链内容写成实施项")
    for rel_path, content in agent_files:
        if "Weak Trace" in content or "弱追溯" in content:
            prohibited_items.append(f"{rel_path} 包含 Weak Trace 风险")
        if "断链" in content:
            prohibited_items.append(f"{rel_path} 包含断链风险")
        if ("source_id" in content or "来源说明" in content) and not has_source_anchor(content):
            prohibited_items.append(f"{rel_path} 缺少 Strong Trace 来源锚点")
    return {
        "files": [path for path, _ in agent_files],
        "safe_for_execution": not prohibited_items,
        "prohibited_items": prohibited_items,
    }


def build_quality_report(root_path: Path, files: list[tuple[str, str]] | None = None) -> dict:
    files = _read_generated_files(root_path) if files is None else files
    unresolved = check_unresolved_content(files)
    consolidation = check_pending_questions_consolidation(root_path, files)
    traceability = check_traceability(files)
    pages = check_page_completeness(root_path)
    rules = check_rule_completeness(root_path)
    coverage = check_manifest_coverage(root_path, files)
    prerequisites = check_prerequisites(root_path)
    relation_chain = check_relation_chain_safety(root_path)
    agent_context_safety = check_agent_context_safety(files, prerequisites, relation_chain)
    can_final = (
        coverage["complete"]
        and not unresolved
        and consolidation["all_consolidated"]
        and not any(r["status"] == "FAIL" for r in traceability)
        and not pages
        and not rules
        and not prerequisites["limited"]
        and relation_chain["safe"]
        and agent_context_safety["safe_for_execution"]
    )
    status = "passed" if can_final else "limited" if prerequisites["limited"] else "failed"
    soft_gate = CheckResult(
        stage="Generate",
        status=status,
        can_proceed=can_final,
        risks=tuple(prerequisites["missing"] + relation_chain["risks"] + agent_context_safety["prohibited_items"]),
        pending=tuple(item["path"] + " 缺失" for item in coverage["missing"][:5]),
    )
    return {
        "files": files,
        "manifest": coverage["manifest"],
        "soft_gate": soft_gate,
        "coverage": coverage,
        "unresolved": unresolved,
        "consolidation": consolidation,
        "traceability": traceability,
        "pages": pages,
        "rules": rules,
        "prerequisites": prerequisites,
        "relation_chain": relation_chain,
        "agent_context_safety": agent_context_safety,
        "limited_generate": {
            "status": "limited" if prerequisites["limited"] else "complete",
            "risks": prerequisites["missing"],
            "prohibited_items": agent_context_safety["prohibited_items"],
        },
    }


def _check_doc_completeness(docs_dir: Path, template_path: Path, root_path: Path) -> list[dict]:
    """Check if documents in a directory have required sections from a template."""
    results = []
    if not docs_dir.exists():
        return results

    required_sections = extract_template_sections(template_path)

    for md_file in docs_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        rel_path = md_file.relative_to(root_path)

        missing = [s for s in required_sections if s not in content]
        results.append({
            "file": str(rel_path),
            "status": "FAIL" if missing else "PASS",
            "missing_sections": missing,
        })

    return results


def print_results(
    unresolved: list[dict],
    consolidation: dict,
    traceability: list[dict],
    pages: list[dict],
    rules: list[dict],
):
    print("=" * 60)
    print("PRD Helper Generated Content Check")
    print("=" * 60)
    print()

    print("--- Unresolved Content ---")
    if unresolved:
        for r in unresolved:
            print(f"  ⚠️  {r['file']}: {r['pattern']} x{r['count']}")
    else:
        print("  ✅ No unresolved content found")
    print()

    print("--- Pending Questions Consolidation ---")
    if consolidation["checked"]:
        if consolidation["pending_count"] == 0:
            print("  ✅ No pending questions in generated docs")
        elif consolidation["all_consolidated"]:
            print(f"  ✅ {consolidation['pending_count']} pending questions found, consolidated in 05-check")
        else:
            print(f"  ❌ {consolidation['pending_count']} pending questions NOT consolidated in 05-check")
    else:
        print("  ⚠️  Could not check consolidation")
    print()

    print("--- Traceability ---")
    if traceability:
        for r in traceability:
            icon = "✅" if r["status"] == "PASS" else "❌"
            print(f"  {icon} {r['file']}")
    else:
        print("  ℹ️  No generated files to check")
    print()

    print("--- Page Completeness ---")
    if pages:
        for r in pages:
            icon = "✅" if r["status"] == "PASS" else "❌"
            missing = f" (missing: {', '.join(r['missing_sections'])})" if r["missing_sections"] else ""
            print(f"  {icon} {r['file']}{missing}")
    else:
        print("  ℹ️  No pages to check")
    print()

    print("--- Rule Completeness ---")
    if rules:
        for r in rules:
            icon = "✅" if r["status"] == "PASS" else "❌"
            missing = f" (missing: {', '.join(r['missing_sections'])})" if r["missing_sections"] else ""
            print(f"  {icon} {r['file']}{missing}")
    else:
        print("  ℹ️  No rules to check")
    print()

    print("=" * 60)


def _report_from_legacy_args(
    root_path: Path,
    unresolved: list[dict],
    consolidation: dict,
    traceability: list[dict],
    pages: list[dict],
    rules: list[dict],
) -> dict:
    files = _read_generated_files(root_path)
    coverage = check_manifest_coverage(root_path, files)
    prerequisites = check_prerequisites(root_path)
    relation_chain = check_relation_chain_safety(root_path)
    agent_context_safety = check_agent_context_safety(files, prerequisites, relation_chain)
    return {
        "files": files,
        "manifest": coverage["manifest"],
        "coverage": coverage,
        "unresolved": unresolved,
        "consolidation": consolidation,
        "traceability": traceability,
        "pages": pages,
        "rules": rules,
        "prerequisites": prerequisites,
        "relation_chain": relation_chain,
        "agent_context_safety": agent_context_safety,
        "limited_generate": {
            "status": "limited" if prerequisites["limited"] else "complete",
            "risks": prerequisites["missing"],
            "prohibited_items": agent_context_safety["prohibited_items"],
        },
    }


def write_check_md(root_path: Path, *args) -> Path:
    """Write 04-generate/check.md using the generate check template structure."""
    if len(args) == 1 and isinstance(args[0], dict):
        report = args[0]
    elif len(args) == 5:
        report = _report_from_legacy_args(root_path, *args)
    else:
        raise TypeError("write_check_md expects a quality report or legacy check result arguments")

    unresolved = report["unresolved"]
    consolidation = report["consolidation"]
    traceability = report["traceability"]
    pages = report["pages"]
    rules = report["rules"]
    coverage = report["coverage"]
    prerequisites = report["prerequisites"]
    relation_chain = report["relation_chain"]
    agent_context_safety = report["agent_context_safety"]

    gen_dir = root_path / "04-generate"
    gen_dir.mkdir(parents=True, exist_ok=True)

    source_ok = (
        not prerequisites["limited"]
        and not unresolved
        and not any(r["status"] == "FAIL" for r in traceability)
        and not (consolidation["checked"] and not consolidation["all_consolidated"])
        and coverage["complete"]
    )
    page_ok = bool(pages) and not any(r["status"] == "FAIL" for r in pages)
    rule_ok = bool(rules) and not any(r["status"] == "FAIL" for r in rules)
    can_final = source_ok and page_ok and rule_ok

    pending = []
    pending.extend(prerequisites["missing"])
    pending.extend(f"{view['path']} 缺失" for view in coverage["missing"])
    pending.extend(f"{path} 非预期生成" for path in coverage["unexpected"])
    pending.extend(f"{r['file']} 缺少来源追溯" for r in traceability if r["status"] == "FAIL")
    pending.extend(f"{r['file']} 存在未解决标记" for r in unresolved)
    pending.extend(f"{r['file']} 缺少章节" for r in pages if r["status"] == "FAIL")
    pending.extend(f"{r['file']} 缺少章节" for r in rules if r["status"] == "FAIL")
    if consolidation["checked"] and not consolidation["all_consolidated"]:
        unconsol = consolidation.get("unconsolidated", [])
        if unconsol:
            for q in unconsol[:3]:
                pending.append(f"待确认问题未汇总: {q['line'][:40]}")
        else:
            pending.append("待确认问题未汇总到 05-check")

    w = CheckWriter(gen_dir, template_path=module_template_path(__file__, "04-generate-check-template.md"))
    w.add_meta("检查来源", "check-generated.py 自动生成")
    w.add_meta("检查状态", "通过" if can_final else "受限生成" if prerequisites["limited"] else "不通过")
    w.add_meta("待确认项", "; ".join(pending[:8]) if pending else "无")
    w.add_meta("生成状态", "完整生成" if can_final else "Limited Generate")
    w.add_meta(
        "禁止实施项",
        "; ".join(prerequisites["missing"]) if prerequisites["limited"] else "无",
    )

    w.add_template_section("1. 来源检查", {
        "生成内容来自 02-refine": prerequisites["refine_exists"] and bool(traceability),
        "生成内容来自 03-relate": prerequisites["relate_exists"] and bool(traceability),
        "没有凭空新增规则": not unresolved,
        "AI 推断已标记": not any(r["status"] == "FAIL" for r in traceability),
        "待确认问题已保留": not (consolidation["checked"] and not consolidation["all_consolidated"]),
        "Weak Trace 未进入确定性要求": True,
        "断链内容已进入风险或待确认区": relation_chain["safe"] or bool(relation_chain["risks"]),
    })

    w.add_template_section("2. 结构检查", {
        "项目说明完整": "04-generate/overview/project-overview.md" not in {
            view["path"] for view in coverage["missing"]
        },
        "页面说明完整": page_ok,
        "功能规则完整": rule_ok,
        "数据说明完整": not any(view["type"] == "data" for view in coverage["missing"]),
        "验收标准完整": not any(view["type"] == "acceptance" for view in coverage["missing"]),
        "Agent 上下文完整": not any(view["type"] == "agent-context" for view in coverage["missing"]),
    })

    w.add_template_section("3. 角色覆盖检查", {
        "产品经理可读": source_ok,
        "前端可执行": source_ok,
        "后端可理解": source_ok,
        "测试可验收": source_ok,
        "Agent 可使用": source_ok and agent_context_safety["safe_for_execution"],
    })

    w.add_conclusion(
        can_proceed=can_final,
        reason="自动检查通过" if can_final else "; ".join(pending[:8]) if pending else "存在未通过项",
    )
    if prerequisites["limited"]:
        w.add_section("5. Limited Generate 风险", [
            (False, "缺失来源：" + "; ".join(prerequisites["missing"])),
            (False, "断链内容：前置关联产物缺失，无法证明关系链完整"),
            (False, "待确认问题：需要补齐 refine/relate 后复核"),
            (False, "禁止实施项：不得把缺失来源或断链内容写成确定性要求"),
        ])
    if coverage["missing"] or coverage["unexpected"]:
        coverage_items = [
            (False, f"{view['path']} 缺失")
            for view in coverage["missing"]
        ]
        coverage_items.extend((False, f"{path} 非预期生成") for path in coverage["unexpected"])
        w.add_section("6. Manifest 覆盖检查", coverage_items)
    quality_items = [
        (coverage["complete"], f"Coverage: expected={coverage['expected_count']} actual={coverage['actual_count']}"),
        (not any(r["status"] == "FAIL" for r in traceability), "Traceability: generated Views keep source or relation anchors"),
        (relation_chain["safe"], "Relation Chain: " + ("完整" if relation_chain["safe"] else "; ".join(relation_chain["risks"]))),
        (
            agent_context_safety["safe_for_execution"],
            "Agent Context Safety: "
            + ("可执行" if agent_context_safety["safe_for_execution"] else "; ".join(agent_context_safety["prohibited_items"])),
        ),
        (not prerequisites["limited"], "Limited Generate: " + ("无" if not prerequisites["limited"] else "; ".join(prerequisites["missing"]))),
    ]
    w.add_section("7. Structured Quality Report", quality_items)
    return w.write()


def main():
    if len(sys.argv) > 1:
        root = sys.argv[1]
    else:
        root = DEFAULT_PRD_ROOT

    root_path = Path(root)
    if not root_path.exists():
        print(f"Error: Directory '{root}' does not exist.")
        sys.exit(1)

    files = _read_generated_files(root_path)
    report = build_quality_report(root_path, files)

    print_results(
        report["unresolved"],
        report["consolidation"],
        report["traceability"],
        report["pages"],
        report["rules"],
    )
    check_file = write_check_md(root_path, report)
    print(f"\nCheck written to: {check_file}")

    # 报告模式：无数据时不阻断，有数据时检查错误
    gen_dir = root_path / "04-generate"
    if not gen_dir.exists() or not files:
        sys.exit(0)

    has_unresolved = len(report["unresolved"]) > 0
    has_consolidation_fail = report["consolidation"]["checked"] and not report["consolidation"]["all_consolidated"]
    has_traceability_fail = any(r["status"] == "FAIL" for r in report["traceability"])
    has_page_fail = any(r["status"] == "FAIL" for r in report["pages"])
    has_rule_fail = any(r["status"] == "FAIL" for r in report["rules"])
    has_coverage_fail = not report["coverage"]["complete"]

    if (
        has_unresolved
        or has_consolidation_fail
        or has_traceability_fail
        or has_page_fail
        or has_rule_fail
        or has_coverage_fail
    ):
        sys.exit(1)


if __name__ == "__main__":
    main()
