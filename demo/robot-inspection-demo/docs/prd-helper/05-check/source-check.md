# 来源追溯检查

## 1. 事实来源追溯

| 事实 | 来源材料 | 来源位置 | 可信度 |
|------|---------|---------|--------|
| fact_001 | 产品口述、会议纪要 | product-voice.md、meeting-notes.md | 高 |
| fact_002 | 产品口述、Agent 对话 | product-voice.md、agent-session.md | 高 |
| fact_003 | 产品口述 | product-voice.md | 高 |
| fact_004 | 产品口述、会议纪要 | product-voice.md、meeting-notes.md | 高 |
| fact_005 | 产品口述、会议纪要 | product-voice.md、meeting-notes.md | 高 |
| fact_006 | 会议纪要 | meeting-notes.md | 高 |
| fact_007 | 会议纪要 | meeting-notes.md | 高 |
| fact_008 | 客户反馈 | customer-feedback.md | 高 |
| fact_009 | 客户反馈 | customer-feedback.md | 中 |
| fact_010 | 客户反馈 | customer-feedback.md | 中 |
| fact_011 | Agent 对话 | agent-session.md | 高 |
| fact_012 | Agent 对话 | agent-session.md | 高 |

## 2. 决策来源追溯

| 决策 | 来源材料 | 状态 |
|------|---------|------|
| decision_001 | 产品口述、会议纪要 | 已确认 |
| decision_002 | 会议纪要 | 已确认 |
| decision_003 | 产品口述、会议纪要 | 已确认 |
| decision_004 | Agent 对话 | 已确认 |
| decision_005 | 会议纪要 | 已确认 |

## 3. 约束来源追溯

| 约束 | 来源材料 | 状态 |
|------|---------|------|
| constraint_001 | 产品口述 | 已确认 |
| constraint_002 | 产品口述、会议纪要 | 已确认 |
| constraint_003 | 会议纪要 | 已确认 |
| constraint_004 | 原型说明 | 已确认 |
| constraint_005 | 会议纪要 | 已确认 |
| constraint_006 | 产品口述 | 已确认 |

## 4. AI 推断标记检查

| 推断 | 标记状态 | 允许进入生成文档 |
|------|---------|----------------|
| assumption_001 | ✅ 已标记 | 是，标记为推断 |
| assumption_002 | ✅ 已标记 | 否，需先确认 |
| assumption_003 | ✅ 已标记 | 是，标记为推断 |
| assumption_004 | ✅ 已标记 | 是，标记为推断 |
| assumption_005 | ✅ 已标记 | 是，标记为推断 |
| assumption_006 | ✅ 已标记 | 否，需先确认 |
| assumption_007 | ✅ 已标记 | 是，标记为推断 |

## 5. 结论

所有关键内容均有来源追溯，AI 推断已明确标记，并覆盖机器人硬件接口、批量导入、现有数据结构和实时位置展示等未明确领域，无无依据结论。
