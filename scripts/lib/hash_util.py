"""
哈希工具：统一内容哈希计算。
"""

import hashlib
from pathlib import Path


def content_hash(text: str) -> str:
    """计算文本内容的 sha256 hash，返回前 16 位十六进制。"""
    return "sha256:" + hashlib.sha256(text.encode()).hexdigest()[:16]


def file_hash(path: Path) -> str:
    """计算文件内容的 sha256 hash，返回前 16 位十六进制。"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()[:16]
