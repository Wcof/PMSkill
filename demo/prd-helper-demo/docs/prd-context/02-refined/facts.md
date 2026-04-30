# 需求事实

## 事实清单

| fact_id | 事实内容 | 来源 | 可信度 | 影响范围 | 关联对象 | 状态 |
|---------|---------|------|--------|---------|---------|------|
| fact-001 | PRD helper 是面向产品经理的产品上下文处理工具 | 01-sources/product-voice.md | 高 | 全局 | 项目定位 | 已确认 |
| fact-002 | 核心链路是采集→精炼→关联→生成 | 01-sources/product-voice.md | 高 | 全局 | 四模块 | 已确认 |
| fact-003 | 检查是贯穿四个模块的质量门禁，不是第五个业务模块 | 01-sources/product-voice.md | 高 | 全局 | 检查机制 | 已确认 |
| fact-004 | AI 辅助开发的主要瓶颈是上下文，不是 prompt | 01-sources/prototype-notes.md | 高 | 全局 | 产品定位 | 已确认 |
| fact-005 | Claude Code、Codex、Cursor、Trae 等 Agent 缺少项目真实背景时容易出错 | 01-sources/prototype-notes.md | 高 | Agent适配 | 工具适配 | 已确认 |
| fact-006 | 多 Agent 协作时需要共享上下文和增量记录 | 01-sources/prototype-notes.md | 高 | 关联/生成 | Context Delta | 已确认 |
| fact-007 | 传统 PRD 主要用于交付、评审和留痕 | 01-sources/meeting-notes.md | 高 | 生成模块 | PRD生成 | 已确认 |
| fact-008 | Agent Context PRD 主要用于让 Agent 快速理解项目上下文 | 01-sources/meeting-notes.md | 高 | 生成模块 | Agent上下文 | 已确认 |
| fact-009 | 不同角色需要不同的上下文：前端看页面、后端看规则和数据、测试看验收、产品看全貌 | 01-sources/meeting-notes.md | 高 | 生成模块 | 角色化输出 | 已确认 |
| fact-010 | v0.1 Demo 的主角应该是 PRD helper 自身 | 01-sources/agent-session.md | 高 | 全局 | Demo场景 | 已确认 |
| fact-011 | 当前采用敏捷开发，希望完整流程闭环 | 01-sources/agent-session.md | 高 | 全局 | 开发方式 | 已确认 |
| fact-012 | 第一版不做平台、不做 UI、不做后台，先用 Skill + Markdown 工作流跑通闭环 | 01-sources/product-voice.md | 高 | 全局 | 项目范围 | 已确认 |
