---
description: 直接精炼采集材料（不强制要求先完成采集）
allowed-tools: Bash
---

# /prd-refine

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

# 运行精炼检查（报告模式，不阻断）
python3 "$skill_root/modules/refine/scripts/check-refine.py" docs/prd-helper || true
```

扫描 `docs/prd-helper/01-collect/` 下的材料，执行精炼流程：

1. 读取 `modules/refine/guide.md` 了解精炼规则
2. 扫描 `01-collect/active/sessions/` 和 `01-collect/passive/` 下的材料
3. 提取事实、背景、目标、决策、约束、冲突、问题和 AI 推断
4. 输出到 `docs/prd-helper/02-refine/`
5. 运行 `check-refine.py` 验证

如果材料为空，提示用户先用 `/prd-start` 采集或直接粘贴内容。
