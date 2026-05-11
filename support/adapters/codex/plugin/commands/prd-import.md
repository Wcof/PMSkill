---
description: 导入第三方文件夹数据作为被动材料
allowed-tools: Bash
---

# /prd-import

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
set -euo pipefail

find_prd_dispatcher() {
  for dir in ".agents/skills/prd-import" ".agents/skills/prd-helper" ".claude/skills/prd-import" ".claude/skills/prd-helper" ".trae/skills/prd-import" ".trae/skills/prd-helper" "."; do
    [ -f "$dir/scripts/prd-command-dispatch.py" ] && { printf '%s\n' "$dir/scripts/prd-command-dispatch.py"; return 0; }
  done
  for dir in \
    "${CODEX_HOME:-$HOME/.codex}/plugins/prd-helper/skills/prd-helper" \
    "${CODEX_HOME:-$HOME/.codex}/local-marketplaces/prd-helper/plugins/prd-helper/skills/prd-helper"; do
    [ -f "$dir/scripts/prd-command-dispatch.py" ] && { printf '%s\n' "$dir/scripts/prd-command-dispatch.py"; return 0; }
  done
  return 1
}

dispatcher="$(find_prd_dispatcher)" || {
  echo "未找到 PRD Helper 命令分发器。请先运行：npx skills@latest add Wcof/PRDContextEngine --all --full-depth"
  exit 1
}

python3 "$dispatcher" import --project . --docs-root docs/prd-helper
```

执行后按用户给定来源完成导入：写入 `docs/prd-helper/01-collect/passive/`，并在 `source-index.csv` 登记来源锚点。无法定位 `locator` 的内容标记为弱追溯，后续只能进入待确认区。

执行后用简短中文说明结果；如果用户使用英文，则用英文说明。
