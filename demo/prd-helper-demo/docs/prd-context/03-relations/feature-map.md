# 功能关联

## 功能清单

| relation_id | 关联功能 | 关联规则 | 来源事实 |
|-------------|---------|---------|---------|
| rel-feat-001 | 采集（collect） | 采集规则：保留原始内容、标记来源和类型 | fact-002, fact-003 |
| rel-feat-002 | 精炼（refine） | 精炼规则：区分事实和推断、标记冲突和待确认 | fact-002, fact-003 |
| rel-feat-003 | 关联（relate） | 关联规则：建立需求→页面→规则→数据→验收关系 | fact-002, fact-003 |
| rel-feat-004 | 生成（generate） | 生成规则：角色化输出、基于 refined 和 relations | fact-002, fact-007, fact-008, fact-009 |
| rel-feat-005 | 检查（check） | 检查规则：每步输出 check.md、最终输出 05-check | fact-003 |
| rel-feat-006 | Context Delta | Delta规则：输出本轮增量、供下轮使用 | fact-006 |
| rel-feat-007 | 工具适配 | 适配规则：支持 Codex/Claude Code/Trae/Generic | fact-005, fact-008 |
| rel-feat-008 | Demo 自举 | 自举规则：使用 PRD helper 自身作为 Demo 场景 | fact-010 |
| rel-feat-009 | 敏捷开发 | 开发规则：完整流程闭环，不缩减计划 | fact-011 |
| rel-feat-010 | 范围约束 | 约束规则：不做 UI/后台/数据库等 | fact-012 |
