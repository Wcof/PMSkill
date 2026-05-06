# /prd-scan

扫描所有 AI 工具的项目 session，并批量导入采集池。

## Workflow

1. 确保项目已初始化
2. 扫描历史 Agent 会话
3. 将命中的会话写入 `01-collect/active/historical/`
4. 更新 `source-index.md`

## 执行

```bash
python3 "{skill_root}/scripts/setup-prd-helper.py" --project . --docs-root "{docs_root}" --agent codex
python3 "{skill_root}/modules/collect/scripts/collect-control.py" scan --root "{docs_root}/01-collect" --project . --docs-root "{docs_root}" --agent codex
```

