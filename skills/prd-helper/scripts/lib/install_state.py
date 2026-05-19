"""Shared install-state helpers for PRD Helper agents."""

from __future__ import annotations

from pathlib import Path

from .command_registry import ALL_COMMAND_NAMES
from .constants import CODEX_LOCAL_MARKETPLACE_NAME, CODEX_LOCAL_MARKETPLACE_REL, CODEX_LOCAL_PLUGIN_REF


LEGACY_COMMAND_FILES = ("prd-init.md", "prd-setup.md")
AGENT_COMMAND_DIRS = {
    "claude-code": ".claude/commands",
    "codex": ".codex/commands",
}


def replace_toml_table(content: str, table_header: str, body: list[str], keep_existing_keys: bool = False) -> str:
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
            existing_keys = {entry.split("=", 1)[0].strip() for entry in body if "=" in entry}
            while index < len(lines) and not lines[index].startswith("["):
                if keep_existing_keys:
                    current = lines[index]
                    current_key = current.split("=", 1)[0].strip() if "=" in current else ""
                    if current.strip() and current_key not in existing_keys:
                        output.append(current)
                index += 1
            continue
        output.append(line)
        index += 1

    if not replaced:
        if output and output[-1] != "":
            output.append("")
        output.extend([table_header, *body])
    return "\n".join(output).rstrip() + "\n"


def render_codex_project_config(content: str, marketplace_root: Path) -> str:
    content = replace_toml_table(
        content,
        f"[marketplaces.{CODEX_LOCAL_MARKETPLACE_NAME}]",
        [
            'source_type = "local"',
            f'source = "{marketplace_root}"',
        ],
    )
    content = replace_toml_table(
        content,
        f'[plugins."{CODEX_LOCAL_PLUGIN_REF}"]',
        ["enabled = true"],
    )
    return replace_toml_table(content, "[features]", ["codex_hooks = true"], keep_existing_keys=True)


def command_files() -> tuple[str, ...]:
    return tuple(f"{name}.md" for name in ALL_COMMAND_NAMES) + LEGACY_COMMAND_FILES


def remove_project_commands(project: Path, agent: str) -> list[Path]:
    commands_rel = AGENT_COMMAND_DIRS.get(agent)
    if not commands_rel:
        return []
    commands_dir = project / commands_rel
    removed: list[Path] = []
    for filename in command_files():
        path = commands_dir / filename
        if path.exists():
            path.unlink()
            removed.append(path)
    return removed
