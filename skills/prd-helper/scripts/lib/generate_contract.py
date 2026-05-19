"""Generate Contract for PRD Helper Views and Limited Generate risks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .id_registry import ACCEPTANCE, DATA, PAGE, RULE


@dataclass(frozen=True)
class GenerateView:
    kind: str
    path: str
    source_ids: tuple[str, ...] = ()
    template: str = ""

    def to_manifest_view(self) -> dict:
        return {
            "type": self.kind,
            "path": self.path,
            "source_ids": list(self.source_ids),
            "template": self.template,
        }


@dataclass(frozen=True)
class GenerateContract:
    status: str
    risks: tuple[str, ...]
    views: tuple[GenerateView, ...]

    def to_manifest(self) -> dict:
        return {
            "status": self.status,
            "risks": list(self.risks),
            "views": [view.to_manifest_view() for view in self.views],
        }


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


def _view(kind: str, path: str, source_ids: tuple[str, ...] = (), template: str = "") -> GenerateView:
    return GenerateView(kind=kind, path=path, source_ids=source_ids, template=template)


def build_generate_contract(root: Path) -> GenerateContract:
    root = Path(root)
    refine_dir = root / "02-refine"
    relate_dir = root / "03-relate"
    risks: list[str] = []
    if not refine_dir.exists() or not any(refine_dir.glob("*.md")):
        risks.append("02-refine/ 缺失")
    if not relate_dir.exists() or not any(relate_dir.glob("*.md")):
        risks.append("03-relate/ 缺失")

    views: list[GenerateView] = [
        _view("overview", "04-generate/overview/project-overview.md", template="04-generate-overview-template.md"),
    ]

    for page_id in _ids_from_file(relate_dir / PAGE.filename, PAGE):
        views.append(_view("page", f"04-generate/pages/{page_id}.md", (page_id,), "04-generate-page-prd-template.md"))
    for rule_id in _ids_from_file(relate_dir / RULE.filename, RULE):
        views.append(_view("rule", f"04-generate/rules/{rule_id}.md", (rule_id,), "04-generate-rule-prd-template.md"))
    for data_id in _ids_from_file(relate_dir / DATA.filename, DATA):
        views.append(_view("data", f"04-generate/data/{data_id}.md", (data_id,), "04-generate-data-prd-template.md"))
    for acceptance_id in _ids_from_file(relate_dir / ACCEPTANCE.filename, ACCEPTANCE):
        views.append(
            _view(
                "acceptance",
                f"04-generate/acceptance/{acceptance_id}.md",
                (acceptance_id,),
                "04-generate-acceptance-template.md",
            )
        )

    for view_type, path in AGENT_CONTEXT_VIEWS:
        views.append(_view("agent-context", path, (view_type,), "04-generate-agent-context-template.md"))
    views.append(_view("check", "04-generate/check.md", template="04-generate-check-template.md"))

    return GenerateContract(
        status="limited" if risks else "complete",
        risks=tuple(risks),
        views=tuple(views),
    )
