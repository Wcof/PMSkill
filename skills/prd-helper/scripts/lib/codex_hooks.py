"""Codex hook installation and cleanup for PRD Helper."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


HOOK_EVENTS = ("UserPromptSubmit", "Stop")
HOOK_SCRIPT_NAME = "claude-capture-hook.py"
HOOKS_FILE_REL = ".codex/hooks.json"
CONFIG_FILE_REL = ".codex/config.toml"


def _default_hook_script() -> Path:
    return Path(__file__).resolve().parents[1] / HOOK_SCRIPT_NAME


def _load_json_object(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        backup = path.with_suffix(path.suffix + ".invalid")
        path.replace(backup)
        print(f"Codex hooks JSON 无法解析，已备份到：{backup}")
        return {}
    return data if isinstance(data, dict) else {}


def _append_unique_hook(settings: dict, event: str, command: str) -> None:
    hooks = settings.setdefault("hooks", {})
    event_hooks = hooks.setdefault(event, [])
    for item in event_hooks:
        if not isinstance(item, dict):
            continue
        for hook in item.get("hooks", []):
            if isinstance(hook, dict) and hook.get("command") == command:
                return
    event_hooks.append({"hooks": [{"type": "command", "command": command}]})


def _replace_toml_table(content: str, table_header: str, body: list[str]) -> str:
    lines = content.splitlines()
    output: list[str] = []
    index = 0
    replaced = False
    while index < len(lines):
        line = lines[index]
        if line.strip() == table_header:
            if output and output[-1] != "":
                output.append("")
            output.extend([table_header, *body])
            replaced = True
            index += 1
            while index < len(lines) and not lines[index].startswith("["):
                index += 1
            continue
        output.append(line)
        index += 1

    if not replaced:
        if output and output[-1] != "":
            output.append("")
        output.extend([table_header, *body])
    return "\n".join(output).rstrip() + "\n"


def ensure_codex_hook_feature(project: Path) -> Path:
    config_file = project / CONFIG_FILE_REL
    config_file.parent.mkdir(parents=True, exist_ok=True)
    content = config_file.read_text(encoding="utf-8") if config_file.exists() else ""
    content = _replace_toml_table(content, "[features]", ["codex_hooks = true"])
    config_file.write_text(content, encoding="utf-8")
    return config_file


def install_codex_hooks(project: Path, docs_root: str, hook_script: Optional[Path] = None) -> Path:
    hooks_file = project / HOOKS_FILE_REL
    hooks_file.parent.mkdir(parents=True, exist_ok=True)
    settings = _load_json_object(hooks_file)
    script = hook_script or _default_hook_script()
    command = f'python3 "{script}" --collect-root {docs_root}/01-collect --agent codex'

    _remove_hooks_from_settings(settings)
    for event in HOOK_EVENTS:
        _append_unique_hook(settings, event, command)

    hooks_file.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ensure_codex_hook_feature(project)
    return hooks_file


def remove_codex_hooks(project: Path) -> Optional[Path]:
    hooks_file = project / HOOKS_FILE_REL
    if not hooks_file.exists():
        _remove_hook_state(project)
        return None
    try:
        settings = json.loads(hooks_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"Codex Hook 配置不是合法 JSON，跳过清理：{hooks_file}")
        _remove_hook_state(project)
        return None

    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        _remove_hook_state(project)
        hooks_file.unlink(missing_ok=True)
        return hooks_file

    changed = _remove_hooks_from_settings(settings)
    if changed:
        if hooks:
            hooks_file.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            hooks_file.unlink(missing_ok=True)
    _remove_hook_state(project)
    return hooks_file if changed else None


def _remove_hooks_from_settings(settings: dict) -> bool:
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        return False

    changed = False
    for event in HOOK_EVENTS:
        event_hooks = hooks.get(event)
        if not isinstance(event_hooks, list):
            continue
        kept = []
        for item in event_hooks:
            item_hooks = item.get("hooks", []) if isinstance(item, dict) else []
            filtered_hooks = [
                hook
                for hook in item_hooks
                if (
                    not isinstance(hook, dict)
                    or HOOK_SCRIPT_NAME not in str(hook.get("command", ""))
                    or "--agent codex" not in str(hook.get("command", ""))
                )
            ]
            if len(filtered_hooks) != len(item_hooks):
                changed = True
            if filtered_hooks:
                new_item = dict(item)
                new_item["hooks"] = filtered_hooks
                kept.append(new_item)
        if kept:
            hooks[event] = kept
        else:
            hooks.pop(event, None)
    if not hooks:
        settings.pop("hooks", None)
    return changed


def _remove_hook_state(project: Path) -> None:
    hook_state = project / ".codex" / "prd-helper"
    if hook_state.exists():
        import shutil

        shutil.rmtree(hook_state)
