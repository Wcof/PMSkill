#!/usr/bin/env python3
"""Generate runner for one-run PRD View production."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "lib").exists())))  # noqa: E501

from lib.constants import DEFAULT_PRD_ROOT
from lib.generate_manifest import build_generate_manifest


def _template_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "templates"


def _load_check_generated():
    path = Path(__file__).resolve().with_name("check-generated.py")
    spec = importlib.util.spec_from_file_location("check_generated", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _read_template(template_name: str) -> str:
    if not template_name:
        return ""
    path = _template_dir() / template_name
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _default_content(view: dict, manifest: dict) -> str:
    source_ids = ", ".join(view.get("source_ids", [])) or "待补充"
    risk_text = "\n".join(f"- {risk}" for risk in manifest.get("risks", [])) or "- 无"
    title = {
        "overview": "# 项目总览",
        "data": f"# 数据说明：{source_ids}",
        "acceptance": f"# 验收说明：{source_ids}",
        "agent-context": f"# Agent Context：{source_ids}",
    }.get(view["type"], f"# {view['type']}：{source_ids}")
    return "\n".join(
        [
            title,
            "",
            "## 来源说明",
            f"- source_ids：{source_ids}",
            "",
            "## Limited Generate 风险",
            risk_text,
            "",
            "## 禁止实施项",
            "- Weak Trace、断链和缺失来源内容不能写成确定性要求。",
            "",
        ]
    )


def _scaffold_content(view: dict, manifest: dict) -> str:
    template = _read_template(view.get("template", ""))
    if template:
        source = ", ".join(view.get("source_ids", [])) or "待补充"
        return (
            template
            .replace("{页面名称}", source)
            .replace("{规则名称}", source)
            .rstrip()
            + "\n"
        )
    return _default_content(view, manifest)


def run_generate(root: Path) -> dict:
    root = Path(root)
    manifest = build_generate_manifest(root)
    summary = {
        "created": [],
        "existing": [],
        "skipped": [],
        "limited": manifest["status"] == "limited",
        "failed": [],
    }

    for view in manifest["views"]:
        if view["type"] == "check":
            summary["skipped"].append(view["path"])
            continue
        target = root / view["path"]
        if target.exists():
            summary["existing"].append(view["path"])
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_scaffold_content(view, manifest), encoding="utf-8")
        summary["created"].append(view["path"])

    checker = _load_check_generated()
    report = checker.build_quality_report(root)
    checker.write_check_md(root, report)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PRD Helper Generate")
    parser.add_argument("root", nargs="?", default=DEFAULT_PRD_ROOT, help="PRD Helper docs root")
    args = parser.parse_args()
    summary = run_generate(Path(args.root))
    print("PRD Generate complete")
    for key in ("created", "existing", "skipped", "failed"):
        print(f"{key}: {len(summary[key])}")
    print(f"limited: {summary['limited']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
