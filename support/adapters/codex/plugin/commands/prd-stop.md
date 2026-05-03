# /prd-stop

停止 PRD Helper 主动采集，扫描 Codex 会话补录未采集的对话，生成采集摘要。

## Workflow

1. 扫描当前项目的 Codex 会话 JSONL，补录未采集的对话轮次
2. 执行采集控制脚本停止采集
3. 生成 collect-summary.md
4. 运行 check-collect.py 验证采集结果
5. 告知用户采集已停止，显示摘要信息

## 执行

首先扫描补录：

```bash
python3 "{skill_root}/modules/collect/scripts/scan-codex-sessions.py" --collect-root "{docs_root}/01-collect" --project . --agent codex
```

然后停止采集：

```bash
python3 "{skill_root}/modules/collect/scripts/collect-control.py" stop --root "{docs_root}/01-collect" --project . --agent codex
```
