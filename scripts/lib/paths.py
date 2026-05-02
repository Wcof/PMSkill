"""
Shared path defaults and constants for PRD Helper scripts.
"""

DEFAULT_COLLECT_ROOT = "docs/prd-helper/01-collect"
DEFAULT_PRD_ROOT = "docs/prd-helper"

# 斜杠命令名，setup 和 remove 共用此列表保持一致
COMMAND_NAMES = (
    "prd-init",
    "prd-start",
    "prd-pause",
    "prd-resume",
    "prd-stop",
    "prd-status",
    "prd-remove",
)
