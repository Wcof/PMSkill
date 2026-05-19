import importlib.util
from pathlib import Path

from scripts.lib.generate_manifest import build_generate_manifest
from modules.generate.scripts.generate import run_generate


def write(path: Path, content: str = "content") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_generate_manifest_lists_all_expected_views_from_relation_artifacts(tmp_path: Path):
    root = tmp_path / "prd-helper"
    write(root / "02-refine" / "facts.md", "## fact_001\n")
    write(root / "03-relate" / "page-map.md", "## page_001\n- 来源事实：fact_001\n")
    write(root / "03-relate" / "rule-map.md", "## rule_001\n- 来源事实：fact_001\n")
    write(root / "03-relate" / "data-map.md", "## data_001\n- 来源事实：fact_001\n")
    write(root / "03-relate" / "acceptance-map.md", "## acceptance_001\n- 来源事实：fact_001\n")

    manifest = build_generate_manifest(root)
    expected_paths = {view["path"] for view in manifest["views"]}

    assert manifest["status"] == "complete"
    assert expected_paths == {
        "04-generate/overview/project-overview.md",
        "04-generate/pages/page_001.md",
        "04-generate/rules/rule_001.md",
        "04-generate/data/data_001.md",
        "04-generate/acceptance/acceptance_001.md",
        "04-generate/agent-context/frontend-context.md",
        "04-generate/agent-context/backend-context.md",
        "04-generate/agent-context/test-context.md",
        "04-generate/agent-context/product-review-context.md",
        "04-generate/check.md",
    }
    assert {view["source_ids"][0] for view in manifest["views"] if view["type"] in {"page", "rule", "data", "acceptance"}} == {
        "page_001",
        "rule_001",
        "data_001",
        "acceptance_001",
    }


def test_generate_manifest_becomes_limited_when_upstream_artifacts_are_missing(tmp_path: Path):
    root = tmp_path / "prd-helper"

    manifest = build_generate_manifest(root)

    assert manifest["status"] == "limited"
    assert "02-refine/ 缺失" in manifest["risks"]
    assert "03-relate/ 缺失" in manifest["risks"]
    assert "04-generate/agent-context/frontend-context.md" in {view["path"] for view in manifest["views"]}


def test_generate_runner_scaffolds_all_manifest_views_and_preserves_existing_content(tmp_path: Path):
    root = tmp_path / "prd-helper"
    write(root / "02-refine" / "facts.md", "## fact_001\n")
    write(root / "03-relate" / "page-map.md", "## page_001\n- 来源事实：fact_001\n")
    write(root / "03-relate" / "rule-map.md", "## rule_001\n- 来源事实：fact_001\n")
    write(root / "04-generate" / "overview" / "project-overview.md", "# 手写项目说明\n\n保留内容\n")

    summary = run_generate(root)

    assert summary["created"]
    assert "04-generate/overview/project-overview.md" in summary["existing"]
    assert (root / "04-generate" / "pages" / "page_001.md").exists()
    assert (root / "04-generate" / "rules" / "rule_001.md").exists()
    assert (root / "04-generate" / "agent-context" / "frontend-context.md").exists()
    assert "保留内容" in (root / "04-generate" / "overview" / "project-overview.md").read_text(encoding="utf-8")
    assert (root / "04-generate" / "check.md").exists()


def test_check_generated_imports_with_dispatch_style_loader():
    path = Path("modules/generate/scripts/check-generated.py").resolve()
    spec = importlib.util.spec_from_file_location("check_generated", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None

    spec.loader.exec_module(module)

    assert hasattr(module, "build_quality_report")
