"""Generate manifest for expected PRD Context Compiler Views."""

from __future__ import annotations

from pathlib import Path

from .id_registry import ACCEPTANCE, DATA, PAGE, RULE


AGENT_CONTEXT_VIEWS = (
    ("frontend-context", "04-generate/agent-context/frontend-context.md"),
    ("backend-context", "04-generate/agent-context/backend-context.md"),
    ("test-context", "04-generate/agent-context/test-context.md"),
    ("product-review-context", "04-generate/agent-context/product-review-context.md"),
)


def _ids_from_file(path: Path, entity) -> list[str]:
    if not path.exists():
        return []
    return sorted(entity.extract_ids(path.read_text(encoding="utf-8")))


def _view(view_type: str, path: str, source_ids: list[str] | None = None, template: str = "") -> dict:
    return {
        "type": view_type,
        "path": path,
        "source_ids": source_ids or [],
        "template": template,
    }


def build_generate_manifest(root: Path) -> dict:
    """Return the expected Generate Views and upstream risks for a PRD root."""
    root = Path(root)
    refine_dir = root / "02-refine"
    relate_dir = root / "03-relate"
    risks: list[str] = []
    if not refine_dir.exists() or not any(refine_dir.glob("*.md")):
        risks.append("02-refine/ 缺失")
    if not relate_dir.exists() or not any(relate_dir.glob("*.md")):
        risks.append("03-relate/ 缺失")

    views = [
        _view("overview", "04-generate/overview/project-overview.md", template="04-generate-overview-template.md"),
    ]

    for page_id in _ids_from_file(relate_dir / PAGE.filename, PAGE):
        views.append(_view("page", f"04-generate/pages/{page_id}.md", [page_id], "04-generate-page-prd-template.md"))
    for rule_id in _ids_from_file(relate_dir / RULE.filename, RULE):
        views.append(_view("rule", f"04-generate/rules/{rule_id}.md", [rule_id], "04-generate-rule-prd-template.md"))
    for data_id in _ids_from_file(relate_dir / DATA.filename, DATA):
        views.append(_view("data", f"04-generate/data/{data_id}.md", [data_id], "04-generate-data-prd-template.md"))
    for acceptance_id in _ids_from_file(relate_dir / ACCEPTANCE.filename, ACCEPTANCE):
        views.append(
            _view(
                "acceptance",
                f"04-generate/acceptance/{acceptance_id}.md",
                [acceptance_id],
                "04-generate-acceptance-template.md",
            )
        )

    for view_type, path in AGENT_CONTEXT_VIEWS:
        views.append(_view("agent-context", path, [view_type], "04-generate-agent-context-template.md"))
    views.append(_view("check", "04-generate/check.md", template="04-generate-check-template.md"))

    return {
        "status": "limited" if risks else "complete",
        "risks": risks,
        "views": views,
    }
