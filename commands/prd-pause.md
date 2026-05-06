---
description: 暂停 PRD Helper 主动采集
allowed-tools: Bash
---

# /prd-pause

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
set -euo pipefail

find_prd_helper_root() {
  for dir in ".claude/skills/prd-helper" ".agents/skills/prd-helper" "."; do
    [ -f "$dir/modules/collect/scripts/collect-control.py" ] && { printf '%s\n' "$dir"; return 0; }
  done
  candidate=$(find "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache" -path "*/prd-helper/*/modules/collect/scripts/collect-control.py" -print -quit 2>/dev/null || true)
  [ -n "$candidate" ] && { dirname "$(dirname "$(dirname "$(dirname "$candidate")")")"; return 0; }
  return 1
}

skill_root="$(find_prd_helper_root)" || {
  echo "未找到 PRD Helper 安装目录。请先运行：npx skills@latest add Wcof/PRDContextEngine --agent claude-code --skill prd-helper -y"
  exit 1
}
python3 "$skill_root/modules/collect/scripts/collect-control.py" pause --root docs/prd-helper/01-collect --project . --docs-root docs/prd-helper --agent claude-code
```
