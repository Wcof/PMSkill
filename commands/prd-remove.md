---
description: 卸载 PRD Helper 并清理 Agent 配置
allowed-tools: Bash
---

# /prd-remove

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
set -euo pipefail

find_prd_helper_root() {
  for dir in ".claude/skills/prd-helper" ".agents/skills/prd-helper" "."; do
    [ -f "$dir/scripts/remove-prd-helper.py" ] && { printf '%s\n' "$dir"; return 0; }
  done
  candidate=$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache" -path "*/prd-helper/*/scripts/remove-prd-helper.py" -print -quit 2>/dev/null || true)
  [ -n "$candidate" ] && { dirname "$(dirname "$candidate")"; return 0; }
  return 1
}

skill_root="$(find_prd_helper_root)" || {
  echo "未找到 PRD Helper 安装目录。"
  exit 1
}

python3 "$skill_root/scripts/remove-prd-helper.py" --project . --agent claude-code
```
