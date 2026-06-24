---
description: 直接精炼采集材料（不强制要求先完成采集）
allowed-tools: Bash
---

# /prd-refine

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
set -euo pipefail

find_prd_dispatcher() {
  for dir in ".agents/skills/prd-refine" ".agents/skills/prd-helper" ".claude/skills/prd-refine" ".claude/skills/prd-helper" ".trae/skills/prd-refine" ".trae/skills/prd-helper" "."; do
    [ -f "$dir/scripts/prd-command-dispatch.py" ] && { printf '%s\n' "$dir/scripts/prd-command-dispatch.py"; return 0; }
  done
  for dir in \
    "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/prd-helper" \
    "${TRAE_HOME:-$HOME/.trae}/skills/prd-helper" \
    "${CODEX_HOME:-$HOME/.codex}/plugins/prd-helper/skills/prd-helper" \
    "${CODEX_HOME:-$HOME/.codex}/local-marketplaces/prd-helper/plugins/prd-helper/skills/prd-helper"; do
    [ -f "$dir/scripts/prd-command-dispatch.py" ] && { printf '%s\n' "$dir/scripts/prd-command-dispatch.py"; return 0; }
  done
  return 1
}

dispatcher="$(find_prd_dispatcher)" || {
  echo "未找到 PRD Helper 命令分发器。请先运行：npx skills@latest add Wcof/PMSkill --all"
  exit 1
}

python3 "$dispatcher" refine --project . --docs-root docs/prd-helper
```

执行后继续完成精炼：把材料拆成事实/决策/约束/目标/冲突/待确认，补齐 Strong Trace（`source_id + path + quote/paraphrase + locator`）。无 locator 的内容只能进入待确认，不能作为确定性要求。

执行后用简短中文说明结果；如果用户使用英文，则用英文说明。
