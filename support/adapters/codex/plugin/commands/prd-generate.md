---
description: 直接生成 PRD 文档（不强制要求先完成关联）
allowed-tools: Bash
---

# /prd-generate

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
set -euo pipefail

find_prd_dispatcher() {
  for dir in ".agents/skills/prd-generate" ".agents/skills/prd-helper" ".claude/skills/prd-generate" ".claude/skills/prd-helper" ".trae/skills/prd-generate" ".trae/skills/prd-helper" "."; do
    [ -f "$dir/scripts/prd-command-dispatch.py" ] && { printf '%s\n' "$dir/scripts/prd-command-dispatch.py"; return 0; }
  done
  candidate=$(find "${CODEX_HOME:-$HOME/.codex}" "${CLAUDE_CONFIG_DIR:-$HOME/.claude}" -path "*/prd-command-dispatch.py" -print -quit 2>/dev/null || true)
  [ -n "$candidate" ] && { printf '%s\n' "$candidate"; return 0; }
  return 1
}

dispatcher="$(find_prd_dispatcher)" || {
  echo "未找到 PRD Helper 命令分发器。请先运行：npx skills@latest add Wcof/PRDContextEngine -y"
  exit 1
}

python3 "$dispatcher" generate --project . --docs-root docs/prd-helper
```

执行后用简短中文说明结果；如果用户使用英文，则用英文说明。
