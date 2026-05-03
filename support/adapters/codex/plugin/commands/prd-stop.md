# /prd-stop

停止 PRD Helper 主动采集，自动扫描 Codex 会话补录未采集的对话，生成采集摘要。

## Workflow

1. 执行采集控制脚本停止采集（内含 Codex 会话扫描补录）
2. 生成 collect-summary.md
3. 告知用户采集已停止，显示摘要信息

## 执行

```bash
python3 "{skill_root}/modules/collect/scripts/collect-control.py" stop --root "{docs_root}/01-collect" --project . --docs-root "{docs_root}" --agent codex
```
