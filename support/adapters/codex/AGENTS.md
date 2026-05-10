<!-- PRD-HELPER:START -->
# PRD Helper Skill - Codex Agent Instructions

## 项目说明

本项目使用 PRD Helper Skill Kit 处理产品上下文。

## 规则来源

完整规则、工作流程、采集命令和检查要求统一见 `support/adapters/canonical-rules.md`。

## Codex 采集规则

当 `capture_mode == on` 时（用户执行了 `/prd-start` 或 `/prd-resume`）：

1. `/prd-start` 会在当前项目安装 Codex hooks，后续轮次优先由 hook 自动采集
2. 不采集 prd- 开头的命令交互（/prd-start、/prd-stop 等）
3. 如果 hook 采集失败，告知用户但不中断工作流
4. `/prd-stop` 会自动扫描 Codex 会话 JSONL 补录遗漏的轮次，无需手动处理
5. 只有在 hook 明确不可用时，才退回手动调用采集脚本

## Codex 命令兜底

Codex 当前项目里如果没有及时刷新 `/` 菜单，也要把下面这些输入当作真实命令处理，而不是普通聊天文本：

- `/prd-helper`
- `/prd-start`
- `/prd-stop`
- `/prd-status`
- `/prd-scan`
- `/prd-import`
- `/prd-refine`
- `/prd-relate`
- `/prd-generate`
- `/prd-discuss`
- `/prd-remove`

处理规则：

1. 如果用户消息以 `/prd-` 开头，优先读取当前项目 `.codex/commands/<command>.md`
2. 如果项目级命令文件不存在，再读取已安装 Skill 中 `support/adapters/codex/plugin/commands/<command>.md`
3. 按命令文件中的 bash 指令执行，不要因为 `/` 菜单没显示就拒绝
4. `/prd-import` 这类允许带参数的命令，要保留命令后的用户参数一起处理

这条兜底规则的目标是：即使 Codex UI 的命令列表没有刷新，只要项目已经执行过 `/prd-helper` 初始化，用户直接输入 `/prd-start` 等命令也必须可用。

## 参考文件

- `support/adapters/canonical-rules.md` — 完整规则
- `SKILL.md` — 流程编排
- `modules/*/guide.md` — 各模块行为约束
- `checks/guide.md` — 检查系统说明
<!-- PRD-HELPER:END -->
