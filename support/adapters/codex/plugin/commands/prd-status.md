# /prd-status

查看 PRD Helper 采集状态。

## Workflow

1. 读取 collect-state.md
2. 显示当前采集模式、会话 ID、轮次数、最近采集时间等信息

## 执行

```bash
python3 "{skill_root}/modules/collect/scripts/collect-control.py" status --root "{docs_root}/01-collect"
```
