---
description: 直接建立关联关系（不强制要求先完成精炼）
allowed-tools: Bash
---

# /prd-relate

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
set -euo pipefail

find_prd_helper_root() {
  for dir in ".agents/skills/prd-helper" "."; do
    [ -f "$dir/scripts/setup-prd-helper.py" ] && { printf '%s\n' "$dir"; return 0; }
  done
  return 1
}

skill_root="$(find_prd_helper_root)" || {
  echo "未找到 PRD Helper 安装目录。"
  exit 1
}

# 确保目录结构存在
python3 "$skill_root/scripts/setup-prd-helper.py" --project . --docs-root docs/prd-helper

# 运行关联检查（报告模式，不阻断）
python3 "$skill_root/modules/relate/scripts/check-relate.py" docs/prd-helper || true
```

扫描 `docs/prd-helper/02-refine/` 下的精炼结果，执行关联流程：

1. 读取 `modules/relate/guide.md` 了解关联规则
2. 扫描 `02-refine/` 下的事实、决策、约束等
3. 建立事实、页面、功能、规则、数据、验收之间的关系
4. 输出到 `docs/prd-helper/03-relate/`
5. 运行 `check-relate.py` 验证

如果精炼结果为空，提示用户先用 `/prd-refine` 精炼或直接粘贴内容。
