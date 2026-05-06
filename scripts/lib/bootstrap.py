"""
Bootstrap — 从任意深度的模块脚本定位 scripts/lib/ 并注入 sys.path。

用法（脚本顶部一行即可）:

    from lib.bootstrap import *  # noqa: F401,F403
"""

import sys
from pathlib import Path


def _find_scripts_dir() -> Path:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "scripts"
        if (candidate / "lib").exists():
            return candidate
    raise RuntimeError("Unable to locate PRD Helper scripts/lib")


_scripts_dir = _find_scripts_dir()
_scripts_str = str(_scripts_dir)
if _scripts_str not in sys.path:
    sys.path.insert(0, _scripts_str)
