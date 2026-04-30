# Context Delta：本轮上下文增量

## 1. 本轮目标

从零创建 PRD Context Skill Kit 工程，跑通 PRD helper 自身产品上下文的完整闭环。

## 2. 新增需求事实

| fact_id | 事实内容 | 来源 | 可信度 |
|---------|---------|------|--------|
| fact-001 | PRD helper 是面向产品经理的产品上下文处理工具 | 01-sources/product-voice.md | 高 |
| fact-002 | 核心链路是采集→精炼→关联→生成 | 01-sources/product-voice.md | 高 |
| fact-003 | 检查是贯穿四个模块的质量门禁 | 01-sources/product-voice.md | 高 |
| fact-004 | AI 辅助开发的主要瓶颈是上下文 | 01-sources/prototype-notes.md | 高 |
| fact-005 | 多 Agent 协作时需要共享上下文和增量记录 | 01-sources/prototype-notes.md | 高 |
| fact-010 | v0.1 Demo 的主角应该是 PRD helper 自身 | 01-sources/agent-session.md | 高 |
| fact-012 | 第一版不做平台、不做 UI、不做后台 | 01-sources/product-voice.md | 高 |

## 3. 新增设计决策

| decision_id | 决策内容 | 决策原因 | 来源 |
|-------------|---------|---------|------|
| decision-001 | 第一版采用通用 Agent Skill 形态 | 先验证核心链路 | 01-sources/product-voice.md |
| decision-002 | 核心流程为采集→精炼→关联→生成 | 完整覆盖链路 | 01-sources/product-voice.md |
| decision-003 | 检查作为横向质量机制 | 贯穿每个步骤 | 01-sources/product-voice.md |
| decision-006 | 生成角色化 Agent 上下文 | 不同角色需要不同视角 | 01-sources/meeting-notes.md |
| decision-007 | 使用 PRD helper 自身作为 Demo | 不会被样例行业带偏 | 01-sources/agent-session.md |

## 4. 新增业务约束

| constraint_id | 约束内容 | 约束类型 | 来源 |
|---------------|---------|---------|------|
| constraint-001 | 不做网页 UI | 业务约束 | 01-sources/product-voice.md |
| constraint-006 | 禁止把 AI 推断写成确定事实 | 业务约束 | 01-sources/product-voice.md |
| constraint-008 | 每步必须输出 check.md | 业务约束 | 01-sources/product-voice.md |

## 5. 修改影响范围

| 受影响文件 | 影响类型 | 说明 |
|-----------|---------|------|
| 全局 | 新建 | 从零创建整个工程 |

## 6. 新增待确认问题

| question_id | 问题内容 | 影响范围 | 优先级 |
|-------------|---------|---------|--------|
| question-001 | Trae 的实际 Skill 文件落点需要验证 | Trae适配 | 中 |
| question-002 | Demo 是否需要包含脚本检查运行结果 | Demo | 低 |
| question-003 | 多轮处理时 Context Delta 如何累积 | 检查机制 | 中 |

## 7. AI 推断项

| assumption_id | 推断内容 | 推断依据 | 可信度 |
|---------------|---------|---------|--------|
| assumption-001 | PRD helper 未来可能需要支持读取本地项目路由 | 产品讨论中提到 v0.3 方向 | 低 |
| assumption-002 | 知识图谱能力可能在后续版本中以轻量方式引入 | 调研中提到知识图谱平台太重 | 低 |
| assumption-003 | Agent 对话摘要的自动采集可能需要 MCP 支持 | Agent 对话信息难以自动沉淀 | 中 |

## 8. 建议同步文件

- [ ] adapters/trae/install.md - 需要在 Trae 环境中验证
- [ ] scripts/ - 需要实际运行验证

## 9. 后续动作建议

1. 在 Trae 环境中验证 Skill 文件落点
2. 运行检查脚本验证结果
3. 邀请研发和测试角色复核 Agent 上下文
4. 设计多轮 Context Delta 累积机制
5. 开始 v0.2 命令自动化脚本开发
