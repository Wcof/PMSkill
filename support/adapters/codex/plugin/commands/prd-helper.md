# /prd-helper

初始化或修复当前项目的 PRD Helper 配置。

## Workflow

1. 创建或修复 `docs/prd-helper/` 目录结构
2. 写入当前项目的 Agent 规则
3. 安装 Codex 插件命令模板
4. 告知用户下一步可以使用 `/prd-start`

## 执行

```bash
python3 "{skill_root}/scripts/setup-prd-helper.py" --project . --docs-root "{docs_root}" --agent codex
```

