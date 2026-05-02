"""
source-index.md 的统一管理。

所有脚本必须通过此模块读写 source-index.md，
不再各自硬编码表头和追加逻辑。
"""

from pathlib import Path


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


def read_indexed_paths(root: Path) -> set[str]:
    """读取 source-index.md 中已索引的文件路径集合。"""
    index_file = root / INDEX_FILE
    if not index_file.exists():
        return set()
    content = index_file.read_text()
    paths = set()
    for line in content.split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) >= 5 and cells[4] and cells[4] not in ("path", "---"):
            paths.add(cells[4])
    return paths


def append_index(root: Path, entry: dict):
    """向 source-index.md 追加一行索引记录。

    如果相同 path 已经存在，则不重复追加。
    """
    index_file = root / INDEX_FILE
    if not index_file.exists():
        index_file.write_text(INDEX_HEADER)
    if entry.get("path") in read_indexed_paths(root):
        return
    content = index_file.read_text()
    cells = [entry.get(col, "") for col in INDEX_COLUMNS]
    row = "| " + " | ".join(cells) + " |\n"
    if not content.endswith("\n"):
        content += "\n"
    content += row
    index_file.write_text(content)
