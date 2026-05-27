from pathlib import Path

from scripts.lib.markdown_util import (
    extract_table_rows,
    extract_table_rows_with_headers,
    extract_template_sections,
    has_field,
)


def test_extract_table_rows_basic():
    content = "| Name | Age |\n|------|-----|\n| Alice | 30 |\n| Bob | 25 |"
    rows = extract_table_rows(content)
    assert len(rows) == 2
    assert rows[0] == {"Name": "Alice", "Age": "30"}
    assert rows[1] == {"Name": "Bob", "Age": "25"}


def test_extract_table_rows_skips_separator():
    content = "| A | B |\n|---|---|\n| 1 | 2 |"
    rows = extract_table_rows(content)
    assert len(rows) == 1
    assert rows[0] == {"A": "1", "B": "2"}


def test_extract_table_rows_empty():
    assert extract_table_rows("") == []
    assert extract_table_rows("no table here") == []


def test_extract_table_rows_mismatched_columns():
    content = "| A | B |\n|---|---|\n| 1 | 2 | 3 |"
    rows = extract_table_rows(content)
    assert len(rows) == 0


def test_extract_table_rows_with_headers_basic():
    content = "| Name | Age |\n|------|-----|\n| Alice | 30 |"
    rows = extract_table_rows_with_headers(content, ("Name", "Age"))
    assert len(rows) == 1
    assert rows[0] == {"Name": "Alice", "Age": "30"}


def test_extract_table_rows_with_headers_skips_non_matching():
    content = (
        "| Other | Table |\n|-------|-------|\n| x | y |\n\n"
        "| Name | Age |\n|------|-----|\n| Alice | 30 |"
    )
    rows = extract_table_rows_with_headers(content, ("Name", "Age"))
    assert len(rows) == 1
    assert rows[0] == {"Name": "Alice", "Age": "30"}


def test_extract_table_rows_with_headers_no_match():
    content = "| A | B |\n|---|---|\n| 1 | 2 |"
    rows = extract_table_rows_with_headers(content, ("Name", "Age"))
    assert rows == []


def test_extract_template_sections_level2(tmp_path: Path):
    template = tmp_path / "t.md"
    template.write_text("# Title\n\n## Section A\n## Section B\n### Sub\n## Section C\n", encoding="utf-8")
    sections = extract_template_sections(template, level=2)
    assert sections == ["## Section A", "## Section B", "## Section C"]


def test_extract_template_sections_level3(tmp_path: Path):
    template = tmp_path / "t.md"
    template.write_text("## Parent\n### Child A\n### Child B\n", encoding="utf-8")
    sections = extract_template_sections(template, level=3)
    assert sections == ["### Child A", "### Child B"]


def test_extract_template_sections_nonexistent(tmp_path: Path):
    assert extract_template_sections(tmp_path / "missing.md") == []


def test_has_field_colon():
    block = "- source_id: test-001\n- path: /some/path\n"
    assert has_field(block, "source_id") is True
    assert has_field(block, "path") is True


def test_has_field_fullwidth_colon():
    block = "- source_id：test-001\n"
    assert has_field(block, "source_id") is True


def test_has_field_empty_value():
    # has_field matches \S+ after colon; "- source_id:" with nothing after is empty
    block = "- source_id:\n- path: /some/path\n"
    # Note: "- source_id: " followed by content on next line still matches due to \S+
    # True empty: colon with no non-whitespace before next line boundary
    assert has_field("- empty:\n", "empty") is False
    assert has_field(block, "path") is True


def test_has_field_missing():
    block = "- path: /some/path\n"
    assert has_field(block, "source_id") is False


def test_has_field_special_chars():
    block = "- file_name: test-file_v2.md\n"
    assert has_field(block, "file_name") is True
