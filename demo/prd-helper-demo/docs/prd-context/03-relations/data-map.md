# 数据关联

## 数据对象清单

| 数据对象 | 所属模块 | 关键字段 | 关系 |
|---------|---------|---------|------|
| source（原始材料） | 采集 | 标题、类型、来源、时间、记录人、原始内容、涉及模块、关键词 | 被精炼为 fact/decision/constraint/conflict/question/assumption |
| fact（需求事实） | 精炼 | fact_id、内容、来源、可信度、影响范围、状态 | 关联到 page/feature/rule |
| decision（设计决策） | 精炼 | decision_id、内容、原因、来源、影响范围、确认状态 | 影响 feature 和 rule |
| constraint（业务约束） | 精炼 | constraint_id、内容、类型、来源、影响页面、影响规则 | 约束 page 和 rule |
| conflict（冲突点） | 精炼 | conflict_id、描述、来源、待决策、影响范围、处理状态 | 影响 fact 和 decision |
| question（待确认问题） | 精炼 | question_id、内容、来源、影响范围、优先级、状态 | 影响 fact/page/rule |
| assumption（AI推断） | 精炼 | assumption_id、内容、依据、可信度、确认问题、状态 | 待确认后可能转为 fact |
| relation（关联关系） | 关联 | relation_id、来源事实、关联页面/功能/规则/数据/验收 | 连接所有对象 |
| page-spec（页面说明） | 生成 | 页面名称、路径、目标、角色、区域、字段、操作、状态 | 来自 page-map |
| rule-spec（规则说明） | 生成 | 规则名称、目标、前置条件、步骤、异常、权限 | 来自 rule-map |
| data-spec（数据说明） | 生成 | 数据域、核心对象、字段语义、状态、生命周期 | 来自 data-map |
| acceptance（验收标准） | 生成 | 功能验收、页面验收、规则验收、异常场景、权限场景 | 来自 acceptance-map |
| agent-context（Agent上下文） | 生成 | 任务背景、相关页面/规则/数据、约束、验收 | 汇总所有相关对象 |
| context-delta（增量记录） | 检查 | 本轮目标、新增事实/决策/约束/问题、影响范围 | 记录本轮变更 |
