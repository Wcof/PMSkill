---
name: prd-refine
description: 直接精炼采集材料（不强制要求先完成采集）
allowed-tools: Bash
---

# /prd-refine

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
python3 .agents/skills/prd-helper/scripts/prd-command-dispatch.py refine --project . --docs-root docs/prd-helper
```

随后读取 `modules/refine/guide.md` 和采集材料，把事实、决策、约束、冲突、问题和推断写入 `docs/prd-helper/02-refine/`。如果当前 Agent 将本 Skill 安装到其他目录，查找已安装 Skill 目录中的 `scripts/prd-command-dispatch.py`，并用同样参数执行。
