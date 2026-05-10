---
name: prd-import
description: 导入第三方文件夹数据作为被动材料
allowed-tools: Bash
---

# /prd-import

请使用用户当前语言响应。中文用户默认中文，英文用户默认英文。

先执行初始化分发：

```bash
python3 .agents/skills/prd-helper/scripts/prd-command-dispatch.py import --project . --docs-root docs/prd-helper
```

然后根据用户给出的文件夹路径，扫描支持的文件并写入 `docs/prd-helper/01-collect/passive/`，同时更新 `docs/prd-helper/01-collect/source-index.md`。如果当前 Agent 将本 Skill 安装到其他目录，查找已安装 Skill 目录中的 `scripts/prd-command-dispatch.py`，并用同样参数执行。
