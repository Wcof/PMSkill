---
description: 直接生成 PRD 文档（不强制要求先完成关联）
allowed-tools: Bash
---

# /prd-generate

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

# 运行生成检查（报告模式，不阻断）
python3 "$skill_root/modules/generate/scripts/check-generated.py" docs/prd-helper || true
```

扫描 `docs/prd-helper/02-refine/` 和 `docs/prd-helper/03-relate/` 下的结果，执行生成流程：

1. 读取 `modules/generate/guide.md` 了解生成规则
2. 扫描精炼和关联结果
3. 生成项目说明、页面说明、规则说明、数据说明、验收标准和 Agent 上下文
4. 输出到 `docs/prd-helper/04-generate/`
5. 运行 `check-generated.py` 验证

如果精炼或关联结果为空，提示用户先用 `/prd-refine` 或 `/prd-relate` 处理。
