"""
source-index.md 的统一管理。

所有脚本必须通过此模块读写 source-index.md，
不再各自硬编码表头和追加逻辑。
"""

from pathlib import Path

from .markdown_util import extract_table_rows_with_headers


INDEX_FILE = "source-index.md"

# source-index 的标准列定义
INDEX_COLUMNS = (
    "source_id",
    "source_time",
    "source_type",
    "source_channel",
    "path",
    "content_hash",
    "metadata_status",
    "noise_hint",
    "status",
)

INDEX_HEADER = (
    "# Source Index\n\n"
    "| source_id | source_time | source_type | source_channel | path | "
    "content_hash | metadata_status | noise_hint | status |\n"
    "|---|---|---|---|---|---|---|---|---|\n"
)


def ensure_index(root: Path):
    """确保 source-index.md 存在，不存在则创建。"""
    index_file = root / INDEX_FILE
    if not index_file.exists():
        index_file.write_text(INDEX_HEADER)


def indexed_paths_from_content(content: str) -> set[str]:
    """从 source-index.md 内容中提取已索引的文件路径集合。"""
    return {
        row["path"]
        for row in extract_table_rows_with_headers(content, INDEX_COLUMNS)
        if row.get("path")
    }


def indexed_source_ids_from_content(content: str) -> set[str]:
    """从 source-index.md 内容中提取已索引的 source_id 集合。"""
    return {
        row["source_id"]
        for row in extract_table_rows_with_headers(content, INDEX_COLUMNS)
        if row.get("source_id")
    }


def read_indexed_paths(root: Path) -> set[str]:
    """读取 source-index.md 中已索引的文件路径集合。"""
    index_file = root / INDEX_FILE
    if not index_file.exists():
        return set()
    return indexed_paths_from_content(index_file.read_text())


def append_index(root: Path, entry: dict):
    """向 source-index.md 追加一行索引记录。

    如果相同 source_id 已经存在，则不重复追加。
    同一 session 文件可有多条索引（不同轮次的 source_id）。
    """
    index_file = root / INDEX_FILE
    if not index_file.exists():
        index_file.write_text(INDEX_HEADER)
    content = index_file.read_text()
    if entry.get("source_id", "") in indexed_source_ids_from_content(content):
        return
    cells = [entry.get(col, "") for col in INDEX_COLUMNS]
    row = "| " + " | ".join(cells) + " |\n"
    if not content.endswith("\n"):
        content += "\n"
    content += row
    index_file.write_text(content)
