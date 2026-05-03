# /prd-resume

恢复 PRD Helper 主动采集。

## Workflow

1. 检查当前采集状态（应为 paused）
2. 执行采集控制脚本恢复采集
3. 告知用户采集已恢复，后续对话将继续记录

## 执行

```bash
python3 "{skill_root}/modules/collect/scripts/collect-control.py" resume --root "{docs_root}/01-collect" --project . --docs-root "{docs_root}" --agent codex
```
