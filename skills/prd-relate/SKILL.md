---
name: prd-relate
description: 直接建立关联关系（不强制要求先完成精炼）
allowed-tools: Bash
---

# /prd-relate

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
python3 .agents/skills/prd-helper/scripts/prd-command-dispatch.py relate --project . --docs-root docs/prd-helper
```

随后读取 `modules/relate/guide.md`，把事实、页面、功能、规则、数据、验收之间的关系写入 `docs/prd-helper/03-relate/`。如果当前 Agent 将本 Skill 安装到其他目录，查找已安装 Skill 目录中的 `scripts/prd-command-dispatch.py`，并用同样参数执行。
