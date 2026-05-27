from pathlib import Path

from scripts.lib.template_path import module_template_path


def test_module_template_path_from_collect_script():
    result = module_template_path(
        "/project/modules/collect/scripts/check-collect.py",
        "01-collect-check-template.md",
    )
    assert str(result).endswith("modules/collect/templates/01-collect-check-template.md")


def test_module_template_path_from_refine_script():
    result = module_template_path(
        "/project/modules/refine/scripts/check-refine.py",
        "02-refine-check-template.md",
    )
    assert "refine/templates/02-refine-check-template.md" in str(result)


def test_module_template_path_resolves_parents():
    # parent.parent from scripts/ goes to modules/<name>/
    result = module_template_path(
        "/repo/modules/generate/scripts/generate.py",
        "template.md",
    )
    assert result == Path("/repo/modules/generate/templates/template.md")
