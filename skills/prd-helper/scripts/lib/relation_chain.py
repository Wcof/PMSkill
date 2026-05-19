"""Relation Chain parsing and reporting helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .id_registry import ACCEPTANCE, ASSUMPTION, CONFLICT, DATA, FACT, FEATURE, PAGE, QUESTION, RULE


SECTION_RE = re.compile(r"^##\s+((?:fact|page|feature|rule|data|acceptance|question|conflict|assumption)[_-]\d+)\s*$")
FIELD_RE = re.compile(r"^\s*-\s*([^:：]+)\s*[:：]\s*(.*\S)?\s*$")
ID_RE = re.compile(r"(?:fact|page|feature|rule|data|acceptance|question|conflict|assumption)[_-]\d+")


@dataclass(frozen=True)
class Block:
    entity_id: str
    file: str
    line: int
    fields: dict[str, list[str]]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _parse_blocks(path: Path) -> dict[str, Block]:
    blocks: dict[str, Block] = {}
    current_id = ""
    current_line = 0
    current_fields: dict[str, list[str]] = {}
    for lineno, raw_line in enumerate(_read(path).splitlines(), start=1):
        line = raw_line.rstrip()
        match = SECTION_RE.match(line)
        if match:
            if current_id:
                blocks[current_id] = Block(current_id, str(path), current_line, current_fields)
            current_id = match.group(1)
            current_line = lineno
            current_fields = {}
            continue
        if not current_id:
            continue
        field = FIELD_RE.match(line)
        if not field:
            continue
        key = field.group(1).strip()
        value = (field.group(2) or "").strip()
        if value:
            current_fields.setdefault(key, []).append(value)
    if current_id:
        blocks[current_id] = Block(current_id, str(path), current_line, current_fields)
    return blocks


def _ids_from_values(values: list[str]) -> list[str]:
    ids: list[str] = []
    for value in values:
        ids.extend(ID_RE.findall(value))
    return ids


def _ids_from_fields(block: Block, *fields: str) -> list[str]:
    ids: list[str] = []
    for field in fields:
        ids.extend(_ids_from_values(block.fields.get(field, [])))
    return ids


def _location(block: Block | None) -> dict | None:
    if not block:
        return None
    return {"file": block.file, "line": block.line, "id": block.entity_id}


def _source_blocks(root: Path) -> dict[str, Block]:
    return _parse_blocks(root / "02-refine" / FACT.filename)


def _relate_blocks(root: Path) -> dict[str, dict[str, Block]]:
    relate_root = root / "03-relate"
    return {
        "page": _parse_blocks(relate_root / PAGE.filename),
        "feature": _parse_blocks(relate_root / FEATURE.filename),
        "rule": _parse_blocks(relate_root / RULE.filename),
        "data": _parse_blocks(relate_root / DATA.filename),
        "acceptance": _parse_blocks(relate_root / ACCEPTANCE.filename),
        "question": _parse_blocks(relate_root / QUESTION.filename),
        "conflict": _parse_blocks(relate_root / CONFLICT.filename),
        "assumption": _parse_blocks(relate_root / ASSUMPTION.filename),
    }


def _find_start(fact_id: str, related: dict[str, dict[str, Block]]) -> tuple[str, Block] | None:
    for kind in ("page", "feature", "rule", "data", "acceptance"):
        for block in related[kind].values():
            if fact_id in _ids_from_fields(block, "来源事实"):
                return kind, block
    return None


def _next_kind(kind: str) -> str | None:
    return {
        "page": "feature",
        "feature": "rule",
        "rule": None,
        "data": None,
        "acceptance": None,
    }.get(kind)


def _next_ids(block: Block, kind: str) -> list[str]:
    if kind == "page":
        return _ids_from_fields(block, "关联功能", "关联规则")
    if kind == "feature":
        return _ids_from_fields(block, "关联规则")
    if kind == "rule":
        return _ids_from_fields(block, "关联数据对象", "关联验收标准")
    return []


def _fact_path(fact_id: str, sources: dict[str, Block], related: dict[str, dict[str, Block]]) -> dict:
    start = _find_start(fact_id, related)
    if not start:
        return {
            "safe": False,
            "path": [],
            "breaks": [{
                "fact_id": fact_id,
                "missing": "page_or_feature",
                "reason": "fact 未关联页面或功能",
                "location": _location(sources.get(fact_id)),
            }],
        }

    kind, block = start
    path = [block.entity_id]
    while True:
        if kind == "rule":
            data_ids = _ids_from_fields(block, "关联数据对象")
            acceptance_ids = _ids_from_fields(block, "关联验收标准")
            if not data_ids:
                return {
                    "safe": False,
                    "path": [],
                    "breaks": [{
                        "fact_id": fact_id,
                        "missing": "data",
                        "reason": "规则缺少关联数据对象",
                        "location": _location(block),
                        "path": path[:],
                    }],
                }
            data_id = data_ids[0]
            if data_id not in related["data"]:
                return {
                    "safe": False,
                    "path": [],
                    "breaks": [{
                        "fact_id": fact_id,
                        "missing": "data",
                        "reason": "规则链路指向的数据对象不存在",
                        "location": _location(block),
                        "target_id": data_id,
                        "path": path[:],
                    }],
                }
            path.append(data_id)
            if not acceptance_ids:
                return {
                    "safe": False,
                    "path": [],
                    "breaks": [{
                        "fact_id": fact_id,
                        "missing": "acceptance",
                        "reason": "规则缺少关联验收标准",
                        "location": _location(block),
                        "path": path[:],
                    }],
                }
            acceptance_id = acceptance_ids[0]
            if acceptance_id not in related["acceptance"]:
                return {
                    "safe": False,
                    "path": [],
                    "breaks": [{
                        "fact_id": fact_id,
                        "missing": "acceptance",
                        "reason": "规则链路指向的验收项不存在",
                        "location": _location(block),
                        "target_id": acceptance_id,
                        "path": path[:],
                    }],
                }
            path.append(acceptance_id)
            return {"safe": True, "path": path, "breaks": []}

        next_kind = _next_kind(kind)
        next_ids = _next_ids(block, kind)
        if not next_ids:
            missing = {
                "page": "page_or_feature",
                "feature": "rule",
            }[kind]
            reason = {
                "page": "页面缺少关联功能或规则",
                "feature": "功能缺少关联规则",
            }[kind]
            return {
                "safe": False,
                "path": [],
                "breaks": [{
                    "fact_id": fact_id,
                    "missing": missing,
                    "reason": reason,
                    "location": _location(block),
                    "path": path[:],
                }],
            }
        next_id = next_ids[0]
        next_block = related[next_kind].get(next_id) if next_kind else None
        if not next_block:
            return {
                "safe": False,
                "path": [],
                "breaks": [{
                    "fact_id": fact_id,
                    "missing": next_kind or "unknown",
                    "reason": f"{kind} 链路指向的 {next_kind} 对象不存在",
                    "location": _location(block),
                    "target_id": next_id,
                    "path": path[:],
                }],
            }
        path.append(next_id)
        kind, block = next_kind, next_block


def parse_relation_chain(root: Path) -> dict:
    root = Path(root)
    sources = _source_blocks(root)
    related = _relate_blocks(root)
    fact_ids = sorted(sources)

    facts: dict[str, dict] = {}
    breaks: list[dict] = []
    for fact_id in fact_ids:
        result = _fact_path(fact_id, sources, related)
        facts[fact_id] = {
            "path": result["path"],
            "breaks": result["breaks"],
            "location": _location(sources.get(fact_id)),
        }
        breaks.extend(result["breaks"])

    context_text = _read(root / "03-relate" / "context-map.md")
    context_ids = set(ID_RE.findall(context_text))

    entities = {kind: set(blocks) for kind, blocks in related.items()}
    impact = {
        "questions_mapped": not entities["question"] or entities["question"] <= context_ids,
        "conflicts_mapped": not entities["conflict"] or entities["conflict"] <= context_ids,
        "assumptions_mapped": not entities["assumption"] or entities["assumption"] <= context_ids,
    }
    isolated = {
        "pages": not entities["page"],
        "features": not entities["feature"],
        "rules": not entities["rule"],
        "data": not entities["data"],
        "acceptance": not entities["acceptance"],
    }
    rule_checks = {
        "fact_to_page_or_feature": not any(item["missing"] == "page_or_feature" for item in breaks),
        "feature_to_rule": not any(item["missing"] == "rule" for item in breaks),
        "rule_to_data": not any(item["missing"] == "data" for item in breaks),
        "rule_to_acceptance": not any(item["missing"] == "acceptance" for item in breaks),
        "page_to_feature_or_rule": all(
            bool(_ids_from_fields(block, "关联功能", "关联规则"))
            for block in related["page"].values()
        ) if entities["page"] else True,
    }

    return {
        "root": str(root),
        "facts": facts,
        "breaks": breaks,
        "entities": entities,
        "impact": impact,
        "isolated": isolated,
        "rule_checks": rule_checks,
        "safe": bool(fact_ids) and not breaks,
    }


def relation_chain_report(chain: dict) -> dict:
    return {
        "safe": chain["safe"] and not any(chain["isolated"].values()) and all(chain["impact"].values()) and all(chain["rule_checks"].values()),
        "facts": chain["facts"],
        "breaks": chain["breaks"],
        "entities": {kind: sorted(ids) for kind, ids in chain["entities"].items()},
        "impact": chain["impact"],
        "isolated": chain["isolated"],
        "rule_checks": chain["rule_checks"],
    }
