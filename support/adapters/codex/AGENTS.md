<!-- PRD-HELPER:START -->
# PRD Helper Skill - Codex Agent Instructions

## 项目说明

本项目使用 PRD Helper Skill Kit 处理产品上下文。

## 规则来源

完整规则、工作流程、采集命令和检查要求统一见 `support/adapters/canonical-rules.md`。

## Codex 采集规则

当 `capture_mode == on` 时（用户执行了 `/prd-start` 或 `/prd-resume`）：

1. 每轮回答结束后，调用采集脚本记录本轮对话
2. 采集命令：
   ```bash
   python3 "{skill_root}/modules/collect/scripts/capture-source.py" --user-query "<用户输入原文>" --agent-answer "<你的回答原文>" --agent codex
   ```
3. 不采集 prd- 开头的命令交互（/prd-start、/prd-stop 等）
4. 如果采集脚本报错，告知用户但不中断工作流
5. `/prd-stop` 会自动扫描 Codex 会话 JSONL 补录遗漏的轮次，无需手动处理

## 参考文件

- `support/adapters/canonical-rules.md` — 完整规则
- `SKILL.md` — 流程编排
- `modules/*/guide.md` — 各模块行为约束
- `checks/guide.md` — 检查系统说明
<!-- PRD-HELPER:END -->
