---
name: prd-start
description: 开启 PRD Helper 主动采集
allowed-tools: Bash
---

# /prd-start

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
python3 .agents/skills/prd-helper/scripts/prd-command-dispatch.py start --project . --docs-root docs/prd-helper
```

如果当前 Agent 将本 Skill 安装到其他目录，查找已安装 Skill 目录中的 `scripts/prd-command-dispatch.py`，并用同样参数执行。
