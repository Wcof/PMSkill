---
description: 导入第三方文件夹数据作为被动材料
allowed-tools: Bash
---

# /prd-import

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
set -euo pipefail

find_prd_helper_root() {
  for dir in ".claude/skills/prd-helper" ".agents/skills/prd-helper" "."; do
    [ -f "$dir/scripts/setup-prd-helper.py" ] && { printf '%s\n' "$dir"; return 0; }
  done
  candidate=$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache" -path "*/prd-helper/*/scripts/setup-prd-helper.py" -print -quit 2>/dev/null || true)
  [ -n "$candidate" ] && { dirname "$(dirname "$candidate")"; return 0; }
  return 1
}

skill_root="$(find_prd_helper_root)" || {
  echo "未找到 PRD Helper 安装目录。请先运行：npx skills@latest add Wcof/PRDContextEngine --agent claude-code --skill prd-helper -y"
  exit 1
}

# 确保目录结构存在
python3 "$skill_root/scripts/setup-prd-helper.py" --project . --docs-root docs/prd-helper --agent claude-code
```

用户指定文件夹路径后，执行以下操作：

1. 扫描指定文件夹下的文件（md/txt/pdf 等格式）
2. 提取文件内容
3. 将内容写入 `docs/prd-helper/01-collect/passive/` 目录
4. 更新 `docs/prd-helper/01-collect/source-index.md`

使用方式：

```
/prd-import /path/to/folder
```

AI 会自动扫描该文件夹下的所有支持格式文件，提取内容并导入为被动材料。
