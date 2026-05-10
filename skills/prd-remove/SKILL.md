---
name: prd-remove
description: 卸载 PRD Helper 并清理 Agent 配置
allowed-tools: Bash
---

# /prd-remove

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

执行：

```bash
python3 .agents/skills/prd-remove/scripts/prd-command-dispatch.py remove --project . --docs-root docs/prd-helper
```

默认保留已经生成的 `docs/prd-helper/` 文档。只有用户明确要求删除产物时，才追加卸载脚本支持的删除参数。如果当前 Agent 将本 Skill 安装到其他目录，查找已安装 Skill 目录中的 `scripts/prd-command-dispatch.py`，并用同样参数执行。
