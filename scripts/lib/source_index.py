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
        index_file.write_text(INDEX_HEADER, encoding="utf-8")


def index_rows_from_content(content: str) -> list[dict]:
    """从 source-index.md 内容中提取标准索引行。"""
    return extract_table_rows_with_headers(content, INDEX_COLUMNS)


def indexed_paths_from_content(content: str) -> set[str]:
    """从 source-index.md 内容中提取已索引的文件路径集合。"""
    return {
        row["path"]
        for row in index_rows_from_content(content)
        if row.get("path")
    }


def indexed_source_ids_from_content(content: str) -> set[str]:
    """从 source-index.md 内容中提取已索引的 source_id 集合。"""
    return {
        row["source_id"]
        for row in index_rows_from_content(content)
        if row.get("source_id")
    }


def indexed_hashes_by_path_from_content(content: str) -> dict[str, set[str]]:
    """从 source-index.md 内容中提取 path -> content_hash 集合。"""
    hashes: dict[str, set[str]] = {}
    for row in index_rows_from_content(content):
        path = row.get("path")
        c_hash = row.get("content_hash")
        if path and c_hash:
            hashes.setdefault(path, set()).add(c_hash)
    return hashes


def read_indexed_paths(root: Path) -> set[str]:
    """读取 source-index.md 中已索引的文件路径集合。"""
    index_file = root / INDEX_FILE
    if not index_file.exists():
        return set()
    return indexed_paths_from_content(index_file.read_text(encoding="utf-8"))


def read_indexed_hashes_by_path(root: Path) -> dict[str, set[str]]:
    """读取 source-index.md 中已索引的 path -> content_hash 集合。"""
    index_file = root / INDEX_FILE
    if not index_file.exists():
        return {}
    return indexed_hashes_by_path_from_content(index_file.read_text(encoding="utf-8"))


def _format_row(entry: dict) -> str:
    cells = [str(entry.get(col, "")).replace("\n", " ") for col in INDEX_COLUMNS]
    return "| " + " | ".join(cells) + " |\n"


def append_index_entries(root: Path, entries: list[dict]) -> int:
    """批量追加索引记录，返回实际追加数量。

    相同 source_id 只追加一次。函数只读写 source-index.md 一次，
    适合批量扫描脚本使用。
    """
    if not entries:
        return 0

    index_file = root / INDEX_FILE
    if not index_file.exists():
        content = INDEX_HEADER
    else:
        content = index_file.read_text(encoding="utf-8")

    source_ids = indexed_source_ids_from_content(content)
    rows: list[str] = []
    for entry in entries:
        source_id = entry.get("source_id", "")
        if source_id in source_ids:
            continue
        rows.append(_format_row(entry))
        source_ids.add(source_id)

    if not rows:
        return 0

    if not content.endswith("\n"):
        content += "\n"
    content += "".join(rows)
    index_file.write_text(content, encoding="utf-8")
    return len(rows)


def append_index(root: Path, entry: dict):
    """向 source-index.md 追加一行索引记录。

    如果相同 source_id 已经存在，则不重复追加。
    同一 session 文件可有多条索引（不同轮次的 source_id）。
    """
    append_index_entries(root, [entry])
