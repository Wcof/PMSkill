---
name: prd-discuss
description: 开启需求研讨模式 — 追问矛盾、模糊术语和未决问题
allowed-tools: Bash, Read
---

# /prd-discuss

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

先执行初始化分发：

```bash
set -euo pipefail

find_prd_dispatcher() {
  for dir in ".agents/skills/prd-discuss" ".agents/skills/prd-helper" ".claude/skills/prd-discuss" ".claude/skills/prd-helper" ".trae/skills/prd-discuss" ".trae/skills/prd-helper" "."; do
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
  echo "未找到 PRD Helper 命令分发器。请先运行：npx skills@latest add Wcof/PRDContextEngine --all"
  exit 1
}

python3 "$dispatcher" discuss --project . --docs-root docs/prd-helper
```

需求研讨是辅助能力，不是第五业务阶段。研讨期间读取 `CONTEXT.md`、`docs/adr/` 和已采集材料，追问矛盾、模糊术语和未决问题；结论回流到 `docs/prd-helper/02-refine/` 和必要的项目上下文文件。如果当前 Agent 将本 Skill 安装到其他目录，查找已安装 Skill 目录中的 `scripts/prd-command-dispatch.py`，并用同样参数执行。
