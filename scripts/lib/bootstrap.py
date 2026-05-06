"""Bootstrap helper for locating scripts/lib from any script depth.

Usage at the top of any script that needs lib.* imports:

    from pathlib import Path
    _scripts = next(
        p / "scripts"
        for p in Path(__file__).resolve().parents
        if (p / "scripts" / "lib").exists()
    )
    import sys; sys.path.insert(0, str(_scripts)) if str(_scripts) not in sys.path else None
    from lib.state import read_collect_state  # now works
"""
