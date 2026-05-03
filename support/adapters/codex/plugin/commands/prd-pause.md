# /prd-pause

暂停 PRD Helper 主动采集。

## Workflow

1. 检查当前采集状态
2. 执行采集控制脚本暂停采集
3. 告知用户采集已暂停，后续对话不会被记录

## 执行

```bash
python3 "{skill_root}/modules/collect/scripts/collect-control.py" pause --root "{docs_root}/01-collect" --project . --agent codex
```
