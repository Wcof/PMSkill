"""Compatibility wrapper for the Generate Contract."""

from __future__ import annotations

from pathlib import Path

from .generate_contract import build_generate_contract


def build_generate_manifest(root: Path) -> dict:
    """Return the expected Generate Views and upstream risks for a PRD root."""
    return build_generate_contract(root).to_manifest()
