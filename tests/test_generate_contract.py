from pathlib import Path

from scripts.lib.generate_contract import build_generate_contract


def test_generate_contract_lists_views_and_limited_risks(tmp_path: Path):
    root = tmp_path / "prd-helper"

    contract = build_generate_contract(root)

    assert contract.status == "limited"
    assert "02-refine/ 缺失" in contract.risks
    assert "03-relate/ 缺失" in contract.risks
    assert "04-generate/overview/project-overview.md" in {view.path for view in contract.views}
    assert "04-generate/agent-context/frontend-context.md" in {view.path for view in contract.views}


def test_generate_contract_derives_relation_views_without_turning_views_into_entities(tmp_path: Path):
    root = tmp_path / "prd-helper"
    (root / "02-refine").mkdir(parents=True)
    (root / "02-refine" / "facts.md").write_text("## fact_001\n", encoding="utf-8")
    relate = root / "03-relate"
    relate.mkdir(parents=True)
    (relate / "page-map.md").write_text("## page_001\n", encoding="utf-8")
    (relate / "rule-map.md").write_text("## rule_001\n", encoding="utf-8")
    (relate / "data-map.md").write_text("## data_001\n", encoding="utf-8")
    (relate / "acceptance-map.md").write_text("## acceptance_001\n", encoding="utf-8")

    contract = build_generate_contract(root)
    views = {view.path: view for view in contract.views}

    assert contract.status == "complete"
    assert views["04-generate/pages/page_001.md"].source_ids == ("page_001",)
    assert views["04-generate/rules/rule_001.md"].kind == "rule"
    assert views["04-generate/data/data_001.md"].kind == "data"
    assert views["04-generate/acceptance/acceptance_001.md"].kind == "acceptance"
