"""
Markdown parsing helpers shared by check scripts.
"""

from pathlib import Path
import re


def extract_table_rows(content: str) -> list[dict]:
    """Extract markdown table rows as dictionaries."""
    rows = []
    headers = []
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if not cells or all(set(c) <= {"-", ":", " "} for c in cells):
            continue
        if not headers:
            headers = cells
        elif len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def extract_template_sections(template_path: Path, level: int = 2) -> list[str]:
    """Extract required heading lines from a template."""
    if not template_path.exists():
        return []
    content = template_path.read_text()
    marker = "#" * level
    return re.findall(rf"^{re.escape(marker)} .+", content, re.MULTILINE)


def has_field(block: str, field: str) -> bool:
    """Return whether a markdown bullet field has a non-empty value. Supports both : and ：."""
    return bool(re.search(rf"^\s*-\s*{re.escape(field)}\s*[:：]\s*\S+", block, re.MULTILINE))
