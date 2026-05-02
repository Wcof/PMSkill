#!/usr/bin/env python3
"""
Compatibility wrapper for older PRD Helper workflows.

Use check-refine.py and check-relate.py directly for module-local checks.
"""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    root = sys.argv[1] if len(sys.argv) > 1 else "docs/prd-helper"
    script_dir = Path(__file__).resolve().parent
    scripts = [script_dir / "check-refine.py", script_dir / "check-relate.py"]
    exit_code = 0
    for script in scripts:
        result = subprocess.run([sys.executable, str(script), root], check=False)
        if result.returncode != 0:
            exit_code = result.returncode
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
