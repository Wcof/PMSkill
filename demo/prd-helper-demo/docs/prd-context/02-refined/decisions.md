# 设计决策

## 决策清单

| decision_id | 决策内容 | 决策原因 | 来源 | 影响范围 | 是否已确认 |
|-------------|---------|---------|------|---------|-----------|
| decision-001 | 第一版采用通用 Agent Skill 形态 | 不做平台、不做 UI，先验证核心链路 | 01-sources/product-voice.md | 全局 | 是 |
| decision-002 | 核心流程为采集→精炼→关联→生成 | 完整覆盖从原始材料到结构化输出的链路 | 01-sources/product-voice.md | 全局 | 是 |
| decision-003 | 检查作为横向质量机制而非独立业务模块 | 检查贯穿每个步骤，不是第五步 | 01-sources/product-voice.md | 检查机制 | 是 |
| decision-004 | 每步必须输出 check.md | 确保质量门禁可追溯 | 01-sources/product-voice.md | 检查机制 | 是 |
| decision-005 | 必须输出 Context Delta | 防止 Agent 对话中新信息丢失 | 01-sources/product-voice.md | 检查机制 | 是 |
| decision-006 | 生成角色化 Agent 上下文 | 不同角色需要不同视角的产品上下文 | 01-sources/meeting-notes.md | 生成模块 | 是 |
| decision-007 | 使用 PRD helper 自身作为 Demo 场景 | 业务对象就是自身，不会被样例行业带偏 | 01-sources/agent-session.md | Demo | 是 |
| decision-008 | 支持 Codex、Claude Code、Trae、通用 Agent 四类适配 | 覆盖主流 Agent 工具 | 01-sources/prototype-notes.md | 适配层 | 是 |
