"""Shared constants for PRD Helper scripts."""

DEFAULT_COLLECT_ROOT = "docs/prd-helper/01-collect"
DEFAULT_PRD_ROOT = "docs/prd-helper"

# /prd-helper 是安装器暴露的根 Skill 入口，用于初始化。
# 这里列出初始化后由脚本生成的 Claude Code 原子命令。
COMMAND_NAMES = (
    "prd-start",
    "prd-stop",
    "prd-status",
    "prd-scan",
    "prd-grill",
    "prd-remove",
)

# Codex 相关常量
CODEX_HOME_ENV = "CODEX_HOME"
CODEX_DEFAULT_HOME = "~/.codex"
CODEX_SESSIONS_REL = "sessions"
CODEX_INDEX_REL = "session_index.jsonl"
CODEX_PLUGIN_DIR = "plugins/prd-helper"

REQUIRED_GENERATED_SUBDIRS = (
    "overview",
    "pages",
    "rules",
    "data",
    "acceptance",
    "agent-context",
)

REQUIRED_GENERATED_FILES = {
    "overview": ("project-overview.md",),
    "agent-context": (
        "frontend-context.md",
        "backend-context.md",
        "test-context.md",
        "product-review-context.md",
    ),
}
