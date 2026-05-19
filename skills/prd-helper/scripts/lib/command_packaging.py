"""Canonical packaging rules for PRD Helper command wrappers."""

from __future__ import annotations

from .command_registry import CommandSpec


def dispatcher_lookup_snippet(command_name: str) -> str:
    helper_dirs = (
        f".agents/skills/{command_name}",
        ".agents/skills/prd-helper",
        f".claude/skills/{command_name}",
        ".claude/skills/prd-helper",
        f".trae/skills/{command_name}",
        ".trae/skills/prd-helper",
        ".",
    )
    dirs = " ".join(f'"{path}"' for path in helper_dirs)
    return "\n".join(
        [
            "find_prd_dispatcher() {",
            f"  for dir in {dirs}; do",
            "    [ -f \"$dir/scripts/prd-command-dispatch.py\" ] && { printf '%s\\n' \"$dir/scripts/prd-command-dispatch.py\"; return 0; }",
            "  done",
            "  for dir in \\",
            "    \"${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/prd-helper\" \\",
            "    \"${TRAE_HOME:-$HOME/.trae}/skills/prd-helper\" \\",
            "    \"${CODEX_HOME:-$HOME/.codex}/plugins/prd-helper/skills/prd-helper\" \\",
            "    \"${CODEX_HOME:-$HOME/.codex}/local-marketplaces/prd-helper/plugins/prd-helper/skills/prd-helper\"; do",
            "    [ -f \"$dir/scripts/prd-command-dispatch.py\" ] && { printf '%s\\n' \"$dir/scripts/prd-command-dispatch.py\"; return 0; }",
            "  done",
            "  return 1",
            "}",
        ]
    )


def render_command_markdown(command: CommandSpec, include_skill_frontmatter: bool) -> str:
    action = command.action
    frontmatter = [
        "---",
    ]
    if include_skill_frontmatter:
        frontmatter.append(f"name: {command.name}")
    frontmatter.extend([
        f"description: {command.zh_description}",
        "allowed-tools: Bash",
        "---",
    ])
    return "\n".join(
        [
            *frontmatter,
            "",
            f"# {command.slash}",
            "",
            "请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。",
            "",
            "执行：",
            "",
            "```bash",
            "set -euo pipefail",
            "",
            dispatcher_lookup_snippet(command.name),
            "",
            'dispatcher="$(find_prd_dispatcher)" || {',
            '  echo "未找到 PRD Helper 命令分发器。请先运行：npx skills@latest add Wcof/PRDContextEngine --all"',
            "  exit 1",
            "}",
            "",
            f'python3 "$dispatcher" {action} --project . --docs-root docs/prd-helper',
            "```",
            "",
        ]
    )
