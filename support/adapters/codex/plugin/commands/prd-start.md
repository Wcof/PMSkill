# /prd-start

开启 PRD Helper 主动采集。

## Workflow

1. 检查项目是否已初始化（docs/prd-helper 是否存在）
2. 执行采集控制脚本开启采集
3. 确认 collect-state.md 写入成功
4. 告知用户采集已开启，后续对话将自动记录

## 执行

```bash
python3 "{skill_root}/modules/collect/scripts/collect-control.py" start --root "{docs_root}/01-collect" --project . --docs-root "{docs_root}" --agent codex
```

如果项目尚未初始化，先执行：

```bash
python3 "{skill_root}/scripts/setup-prd-helper.py" --project . --docs-root "{docs_root}" --agent codex
```
