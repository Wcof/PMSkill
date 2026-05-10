---
name: prd-generate
description: 直接生成 PRD 文档（不强制要求先完成关联）
allowed-tools: Bash
---

# /prd-generate

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
python3 .agents/skills/prd-helper/scripts/prd-command-dispatch.py generate --project . --docs-root docs/prd-helper
```

当前置产物缺失或检查未通过时，生成结果必须是 Limited Generate：显式标记缺失来源、断链、待确认问题和禁止实施项。如果当前 Agent 将本 Skill 安装到其他目录，查找已安装 Skill 目录中的 `scripts/prd-command-dispatch.py`，并用同样参数执行。
