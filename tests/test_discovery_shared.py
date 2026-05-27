"""Tests for discovery_shared.py pure functions."""

import json
from pathlib import Path

from scripts.lib.discovery_shared import (
    Session,
    extract_text,
    is_subpath,
    iter_jsonl_files,
    read_jsonl,
    read_workspace_folder,
)


# --- Session ---

def test_session_attributes():
    s = Session(id="s1", turns=[("q", "a", "t")], path="/p", name="n")
    assert s.id == "s1"
    assert s.name == "n"
    assert s.path == "/p"
    assert s.turns == [("q", "a", "t")]


def test_session_defaults():
    s = Session(id="s2", turns=[])
    assert s.path == ""
    assert s.name == ""


# --- read_jsonl ---

def test_read_jsonl_basic(tmp_path: Path):
    f = tmp_path / "test.jsonl"
    f.write_text('{"a": 1}\n{"b": 2}\n', encoding="utf-8")
    result = read_jsonl(f)
    assert len(result) == 2
    assert result[0] == {"a": 1}
    assert result[1] == {"b": 2}


def test_read_jsonl_skips_blank_and_invalid(tmp_path: Path):
    f = tmp_path / "test.jsonl"
    f.write_text('{"a": 1}\n\nnot json\n{"b": 2}\n', encoding="utf-8")
    result = read_jsonl(f)
    assert len(result) == 2


def test_read_jsonl_empty(tmp_path: Path):
    f = tmp_path / "empty.jsonl"
    f.write_text("", encoding="utf-8")
    assert read_jsonl(f) == []


# --- read_workspace_folder ---

def test_read_workspace_folder_file_uri(tmp_path: Path):
    ws = tmp_path / "workspace.json"
    ws.write_text(json.dumps({"folder": "file:///Users/test/project"}), encoding="utf-8")
    assert read_workspace_folder(tmp_path) == "/Users/test/project"


def test_read_workspace_folder_encoded(tmp_path: Path):
    ws = tmp_path / "workspace.json"
    ws.write_text(json.dumps({"folder": "file:///Users/test/my%20project"}), encoding="utf-8")
    assert read_workspace_folder(tmp_path) == "/Users/test/my project"


def test_read_workspace_folder_missing(tmp_path: Path):
    assert read_workspace_folder(tmp_path) is None


def test_read_workspace_folder_invalid_json(tmp_path: Path):
    ws = tmp_path / "workspace.json"
    ws.write_text("not json", encoding="utf-8")
    assert read_workspace_folder(tmp_path) is None


def test_read_workspace_folder_empty_folder(tmp_path: Path):
    ws = tmp_path / "workspace.json"
    ws.write_text(json.dumps({"folder": ""}), encoding="utf-8")
    assert read_workspace_folder(tmp_path) is None


# --- extract_text ---

def test_extract_text_string():
    assert extract_text("hello") == "hello"


def test_extract_text_list_of_dicts():
    content = [{"text": "a"}, {"text": "b"}]
    assert extract_text(content) == "a\nb"


def test_extract_text_list_with_type_filter():
    content = [{"type": "text", "text": "ok"}, {"type": "image", "text": "skip"}]
    assert extract_text(content, accepted_types=("text",)) == "ok"


def test_extract_text_list_with_string_items():
    content = ["plain", {"text": "dict"}]
    assert extract_text(content) == "plain\ndict"


def test_extract_text_non_string_non_list():
    assert extract_text(42) == ""
    assert extract_text(None) == ""


def test_extract_text_empty_list():
    assert extract_text([]) == ""


def test_extract_text_empty_text_skipped():
    content = [{"text": ""}, {"text": "ok"}]
    assert extract_text(content) == "ok"


# --- is_subpath ---

def test_is_subpath_same():
    assert is_subpath("/a/b", "/a/b") is True


def test_is_subpath_child():
    assert is_subpath("/a/b/c", "/a/b") is True


def test_is_subpath_not_child():
    assert is_subpath("/a/bc", "/a/b") is False


def test_is_subpath_trailing_slash():
    assert is_subpath("/a/b/c", "/a/b/") is True


# --- iter_jsonl_files ---

def test_iter_jsonl_files_basic(tmp_path: Path):
    (tmp_path / "a.jsonl").write_text("{}", encoding="utf-8")
    (tmp_path / "b.jsonl").write_text("{}", encoding="utf-8")
    (tmp_path / "c.txt").write_text("x", encoding="utf-8")
    results = list(iter_jsonl_files(tmp_path))
    assert len(results) == 2
    assert all(stem in ("a", "b") for _, stem in results)


def test_iter_jsonl_files_recursive(tmp_path: Path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "deep.jsonl").write_text("{}", encoding="utf-8")
    (tmp_path / "shallow.jsonl").write_text("{}", encoding="utf-8")
    results = list(iter_jsonl_files(tmp_path, recursive=True))
    assert len(results) == 2


def test_iter_jsonl_files_empty(tmp_path: Path):
    assert list(iter_jsonl_files(tmp_path)) == []
