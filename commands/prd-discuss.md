---
description: 开启需求研讨模式 — 追问矛盾、模糊术语和未决问题
allowed-tools: Bash
---

# /prd-discuss

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
set -euo pipefail

find_prd_dispatcher() {
  for dir in ".agents/skills/prd-discuss" ".agents/skills/prd-helper" ".claude/skills/prd-discuss" ".claude/skills/prd-helper" ".trae/skills/prd-discuss" ".trae/skills/prd-helper" "."; do
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

python3 "$dispatcher" discuss --project . --docs-root docs/prd-helper
```

然后进入研讨模式：基于 `CONTEXT.md`、`docs/adr/`、`docs/prd-helper/01-collect/` 与当前会话，追问术语歧义、目标冲突、约束缺失和待确认问题；将结论沉淀到 `docs/prd-helper/02-refine/`（facts/decisions/constraints/questions/conflicts）。

执行后用简短中文说明结果；如果用户使用英文，则用英文说明。
