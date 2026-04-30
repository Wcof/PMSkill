# 上下文关联

## Agent 对话增量关联

| relation_id | Agent 对话增量 | 相关 PRD 文件 | 影响 |
|-------------|---------------|--------------|------|
| rel-ctx-001 | Agent 误认 Demo 场景为巡检机器人 | demo/prd-helper-demo/ | 纠正 Demo 场景为 PRD helper 自身 |
| rel-ctx-002 | Agent 建议缩减 MVP | docs/development-plan.md | 用户纠正：保持完整流程闭环 |
| rel-ctx-003 | 当前 PRDHelper 已有工程结构 | skills/prd-context/ | 参考现有结构设计新 Skill Kit |

## 跨模块影响

| 来源模块 | 影响模块 | 影响说明 |
|---------|---------|---------|
| 采集 | 精炼 | 原始材料质量直接影响精炼结果 |
| 精炼 | 关联 | 事实和决策的完整性影响关联覆盖 |
| 关联 | 生成 | 关系完整性影响生成文档质量 |
| 检查 | 全局 | 检查结果可能触发前序模块的修正 |
