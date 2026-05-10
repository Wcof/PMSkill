import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_dispatcher():
    path = ROOT / "scripts" / "prd-command-dispatch.py"
    spec = importlib.util.spec_from_file_location("prd_command_dispatch", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_detect_agent_prefers_codex_project(tmp_path: Path):
    module = load_dispatcher()
    (tmp_path / ".codex").mkdir()
    (tmp_path / ".claude").mkdir()

    assert module.detect_agent(tmp_path, {}) == "codex"


def test_detect_agent_supports_claude_and_trae(tmp_path: Path):
    module = load_dispatcher()

    (tmp_path / ".claude").mkdir()
    assert module.detect_agent(tmp_path, {}) == "claude-code"

    (tmp_path / ".claude").rmdir()
    (tmp_path / ".trae").mkdir()
    assert module.detect_agent(tmp_path, {}) == "trae"


def test_find_skill_root_uses_local_installed_helper(tmp_path: Path):
    module = load_dispatcher()
    skill_root = tmp_path / ".agents" / "skills" / "prd-helper"
    (skill_root / "scripts").mkdir(parents=True)
    (skill_root / "scripts" / "setup-prd-helper.py").write_text("", encoding="utf-8")

    assert module.find_skill_root(tmp_path, {}) == skill_root


def test_start_dispatch_runs_setup_before_collect_start(tmp_path: Path, monkeypatch):
    module = load_dispatcher()
    calls = []
    skill_root = tmp_path / ".agents" / "skills" / "prd-helper"
    (skill_root / "scripts").mkdir(parents=True)
    (skill_root / "modules" / "collect" / "scripts").mkdir(parents=True)
    (skill_root / "scripts" / "setup-prd-helper.py").write_text("", encoding="utf-8")
    (skill_root / "modules" / "collect" / "scripts" / "collect-control.py").write_text("", encoding="utf-8")

    def fake_run(cmd, cwd, check):
        calls.append(cmd)
        class Result:
            returncode = 0
        return Result()

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["prd-command-dispatch.py", "start", "--project", str(tmp_path)])

    assert module.main() == 0
    assert calls[0][1].endswith("setup-prd-helper.py")
    assert calls[0][-1] == "claude-code"
    assert calls[1][1].endswith("collect-control.py")
    assert calls[1][2] == "start"


def test_remove_dispatch_does_not_run_setup(tmp_path: Path, monkeypatch):
    module = load_dispatcher()
    calls = []
    skill_root = tmp_path / ".agents" / "skills" / "prd-helper"
    (skill_root / "scripts").mkdir(parents=True)
    (skill_root / "scripts" / "setup-prd-helper.py").write_text("", encoding="utf-8")
    (skill_root / "scripts" / "remove-prd-helper.py").write_text("", encoding="utf-8")

    def fake_run(cmd, cwd, check):
        calls.append(cmd)
        class Result:
            returncode = 0
        return Result()

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["prd-command-dispatch.py", "remove", "--project", str(tmp_path)])

    assert module.main() == 0
    assert len(calls) == 1
    assert calls[0][1].endswith("remove-prd-helper.py")


def test_generate_dispatch_runs_limited_generate_runner(tmp_path: Path, monkeypatch):
    module = load_dispatcher()
    calls = []
    skill_root = tmp_path / ".agents" / "skills" / "prd-helper"
    (skill_root / "scripts").mkdir(parents=True)
    (skill_root / "modules" / "generate" / "scripts").mkdir(parents=True)
    (skill_root / "scripts" / "setup-prd-helper.py").write_text("", encoding="utf-8")
    (skill_root / "modules" / "generate" / "scripts" / "generate.py").write_text("", encoding="utf-8")

    def fake_run(cmd, cwd, check):
        calls.append(cmd)
        class Result:
            returncode = 0
        return Result()

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["prd-command-dispatch.py", "generate", "--project", str(tmp_path)])

    assert module.main() == 0
    assert calls[0][1].endswith("setup-prd-helper.py")
    assert calls[1][1].endswith("generate.py")
    assert calls[1][2] == "docs/prd-helper"


def test_detect_agent_uses_codex_when_project_has_codex_dir(tmp_path: Path):
    module = load_dispatcher()
    (tmp_path / ".codex").mkdir()
    assert module.detect_agent(tmp_path, {}) == "codex"


def test_diagnose_prints_selected_runtime_and_agent(tmp_path: Path, monkeypatch, capsys):
    module = load_dispatcher()
    calls = []
    skill_root = tmp_path / ".agents" / "skills" / "prd-helper"
    (skill_root / "scripts").mkdir(parents=True)
    (skill_root / "scripts" / "setup-prd-helper.py").write_text("", encoding="utf-8")
    (skill_root / "modules" / "collect" / "scripts").mkdir(parents=True)
    (skill_root / "modules" / "collect" / "scripts" / "collect-control.py").write_text("", encoding="utf-8")

    def fake_run(cmd, cwd, check):
        calls.append(cmd)
        class Result:
            returncode = 0
        return Result()

    monkeypatch.setattr(module.subprocess, "run", fake_run)
    monkeypatch.setattr(sys, "argv", ["prd-command-dispatch.py", "--diagnose", "start", "--project", str(tmp_path)])
    assert module.main() == 0
    err = capsys.readouterr().err
    assert "[prd-dispatch] project=" in err
    assert "[prd-dispatch] skill_root=" in err
    assert "[prd-dispatch] agent=" in err
