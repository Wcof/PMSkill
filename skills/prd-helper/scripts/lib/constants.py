"""Shared constants for PRD Helper scripts."""

from .command_registry import GENERATED_COMMAND_NAMES

DEFAULT_COLLECT_ROOT = "docs/prd-helper/01-collect"
DEFAULT_PRD_ROOT = "docs/prd-helper"

# /prd-helper 是安装器暴露的根 Skill 入口，用于初始化。
# 这里列出初始化后由脚本生成的原子命令，并从命令注册表派生。
COMMAND_NAMES = GENERATED_COMMAND_NAMES

# Codex 相关常量
CODEX_HOME_ENV = "CODEX_HOME"
CODEX_DEFAULT_HOME = "~/.codex"
CODEX_SESSIONS_REL = "sessions"
CODEX_INDEX_REL = "session_index.jsonl"
CODEX_PLUGIN_DIR = "plugins/prd-helper"
CODEX_LOCAL_MARKETPLACE_NAME = "prd-helper-local"
CODEX_LOCAL_MARKETPLACE_REL = "local-marketplaces/prd-helper"
CODEX_LOCAL_PLUGIN_REF = f"prd-helper@{CODEX_LOCAL_MARKETPLACE_NAME}"
CODEX_TMP_PLUGIN_CACHE_REL = ".tmp/plugins"
CODEX_TMP_PLUGIN_SHA_REL = ".tmp/plugins.sha"
CODEX_TMP_MARKETPLACES_REL = ".tmp/marketplaces"
CODEX_TMP_REMOTE_SYNC_REL = ".tmp/app-server-remote-plugin-sync-v1"

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
