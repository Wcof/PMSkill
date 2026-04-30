# 产品复核上下文

## 任务背景

PRD Context Skill Kit 是一个通用 Agent Skill 套件，用于处理产品上下文。产品经理需要复核整个流程的输出，确认事实、决策、约束、冲突和待确认问题。

## 相关页面

| 页面名称 | 页面路径 | 关键内容 |
|---------|---------|---------|
| PRD helper 上下文处理流程 | docs/prd-context/ | 采集→精炼→关联→生成→检查的完整流程 |

## 相关规则

| 规则名称 | 规则要点 |
|---------|---------|
| 精炼规则 | 区分事实和推断、标记冲突和待确认 |
| 检查规则 | 每步输出 check.md，最终输出 05-check |

## 相关数据

| 数据对象 | 关键字段 | 关系 |
|---------|---------|------|
| fact | fact_id、内容、来源、可信度、状态 | 需要确认 |
| decision | decision_id、内容、原因、确认状态 | 需要确认 |
| constraint | constraint_id、内容、类型 | 需要确认 |
| conflict | conflict_id、描述、处理状态 | 需要裁决 |
| question | question_id、内容、优先级、状态 | 需要回答 |
| assumption | assumption_id、内容、可信度、状态 | 需要确认 |
| context-delta | 本轮目标、新增内容、后续动作 | 需要复核 |

## 关键约束

- 不允许把 AI 推断当成确定事实
- 必须区分事实、推断、冲突、待确认
- 每步必须有 check.md

## 不可推断内容

- 不可代替产品经理确认事实
- 不可代替产品经理裁决冲突
- 不可代替产品经理回答待确认问题

## 待确认问题

- question-001: Trae 的实际 Skill 文件落点需要验证
- question-002: Demo 是否需要包含脚本检查运行结果
- question-003: 多轮处理时 Context Delta 如何累积

## 验收标准

- [ ] 所有事实已确认或标记为待确认
- [ ] 所有决策已确认
- [ ] 所有冲突已裁决或标记为待处理
- [ ] 所有待确认问题已回答或标记为待确认
- [ ] 所有 AI 推断已确认或标记为待确认
- [ ] Context Delta 已复核

## 执行建议

1. 先阅读 02-refined/ 下的精炼结果
2. 确认 facts.md 中的事实
3. 确认 decisions.md 中的决策
4. 裁决 conflicts.md 中的冲突
5. 回答 questions.md 中的问题
6. 确认 assumptions.md 中的推断
7. 复核 05-check/context-delta.md 中的增量记录
