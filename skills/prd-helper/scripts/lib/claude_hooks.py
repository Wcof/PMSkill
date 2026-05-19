"""Claude Code hook installation and cleanup for PRD Helper."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


HOOK_EVENTS = ("UserPromptSubmit", "Stop")
HOOK_SCRIPT_NAME = "claude-capture-hook.py"


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
        print(f"Claude settings JSON 无法解析，已备份到：{backup}")
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


def install_claude_hooks(project: Path, docs_root: str, hook_script: Optional[Path] = None) -> Path:
    settings_file = project / ".claude" / "settings.json"
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    settings = _load_json_object(settings_file)
    script = hook_script or _default_hook_script()
    command = f'python3 "{script}" --collect-root {docs_root}/01-collect --agent claude-code'

    _remove_hooks_from_settings(settings)
    for event in HOOK_EVENTS:
        _append_unique_hook(settings, event, command)

    settings_file.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return settings_file


def remove_claude_hooks(project: Path) -> Optional[Path]:
    settings_file = project / ".claude" / "settings.json"
    if not settings_file.exists():
        _remove_hook_state(project)
        return None
    try:
        settings = json.loads(settings_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"Claude Code Hook 配置不是合法 JSON，跳过清理：{settings_file}")
        _remove_hook_state(project)
        return None
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        _remove_hook_state(project)
        return settings_file

    changed = _remove_hooks_from_settings(settings)
    if changed:
        if not hooks:
            settings.pop("hooks", None)
        settings_file.write_text(json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    _remove_hook_state(project)
    return settings_file if changed else None


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
                if not isinstance(hook, dict) or HOOK_SCRIPT_NAME not in str(hook.get("command", ""))
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
    hook_state = project / ".claude" / "prd-helper"
    if hook_state.exists():
        import shutil

        shutil.rmtree(hook_state)
