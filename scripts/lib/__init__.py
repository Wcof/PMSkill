"""
PRD Helper 共享库。

所有采集脚本通过此包共享状态管理、索引管理、时间工具和哈希工具。
"""

from .state import read_collect_state, write_collect_state, require_state, STATE_KEYS
from .source_index import ensure_index, read_indexed_paths, append_index, INDEX_COLUMNS, INDEX_HEADER
from .time_util import TZ, now_iso, now_id
from .hash_util import content_hash, file_hash
from .markdown_util import extract_table_rows, extract_table_rows_with_headers, extract_template_sections, has_field
from .constants import COMMAND_NAMES, REQUIRED_GENERATED_SUBDIRS, REQUIRED_GENERATED_FILES
from .constants import DEFAULT_COLLECT_ROOT, DEFAULT_PRD_ROOT
from .command_registry import ALL_COMMANDS, GENERATED_COMMANDS, command_by_name
from .metadata import FIELD_ALIASES, metadata_status_for_text
from .claude_hooks import install_claude_hooks, remove_claude_hooks
from . import id_registry
