"""Shared sys.path bootstrap for module scripts.

Replaces the duplicated sys.path.insert one-liner in all 9 module scripts.

Usage (3 lines, replaces 1 long line):
    import sys; from pathlib import Path
    sys.path.insert(0, str(next(p / "scripts" for p in Path(__file__).resolve().parents if (p / "scripts" / "_bootstrap.py").exists())))  # noqa: E501
    from _bootstrap import setup_path; setup_path(__file__)

After these 3 lines, `from lib.xxx import ...` works as before.
The first line adds scripts/ so _bootstrap can be imported;
setup_path ensures scripts/lib/ is also on sys.path.
"""


def setup_path(script: str) -> None:
    """Add scripts/ to sys.path so `from lib.xxx import ...` works."""
    import sys
    from pathlib import Path
    root = next(
        p for p in Path(script).resolve().parents
        if (p / "scripts" / "lib").exists()
    )
    scripts = str(root / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
