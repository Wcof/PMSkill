"""从模块脚本位置定位对应模块的 templates/ 目录。"""

from pathlib import Path


def module_template_path(script_file: str, template_name: str) -> Path:
    """从 modules/<name>/scripts/ 下的脚本解析 modules/<name>/templates/ 下的模板路径。"""
    return Path(script_file).resolve().parent.parent / "templates" / template_name
