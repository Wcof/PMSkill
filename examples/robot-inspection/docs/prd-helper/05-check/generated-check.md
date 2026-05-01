# 生成内容检查

## 1. 结构完整性

| 文档类型 | 文件 | 状态 |
|---------|------|------|
| 项目说明 | overview/project-overview.md | ✅ |
| 页面说明 | pages/inspection-point-management.md | ✅ |
| 功能规则 | rules/inspection-point-rule.md | ✅ |
| 数据说明 | data/inspection-domain-data.md | ✅ |
| 验收标准 | acceptance/inspection-point-acceptance.md | ✅ |
| 前端上下文 | agent-context/frontend-context.md | ✅ |
| 后端上下文 | agent-context/backend-context.md | ✅ |
| 测试上下文 | agent-context/test-context.md | ✅ |
| 产品评审上下文 | agent-context/product-review-context.md | ✅ |

## 2. 内容质量检查

- [x] 页面说明包含：目标、区域、字段、操作、状态
- [x] 功能规则包含：前置条件、执行步骤、异常、权限
- [x] 数据说明包含：对象、字段、关系、状态
- [x] 验收标准包含：功能、页面、规则、异常、权限
- [x] Agent 上下文包含：任务背景、相关页面/规则/数据、待确认问题
- [x] 生成文档包含来源说明或 fact/rule/data/acceptance 关联标识
- [x] 生成文档未遗漏待确认问题，待确认问题已传递到 05-check

## 3. 待确认问题保留检查

| 待确认问题 | 保留位置 | 状态 |
|-----------|---------|------|
| question_001 | 页面说明、规则说明、Agent 上下文 | ✅ |
| question_002 | 数据说明、Agent 上下文 | ✅ |
| question_003 | 关联图 | ✅ |
| question_004 | 页面说明、规则说明、Agent 上下文 | ✅ |

## 4. 溯源检查

| 文档 | 溯源状态 |
|------|---------|
| overview/project-overview.md | ✅ |
| pages/inspection-point-management.md | ✅ |
| rules/inspection-point-rule.md | ✅ |
| data/inspection-domain-data.md | ✅ |
| acceptance/inspection-point-acceptance.md | ✅ |
| agent-context/frontend-context.md | ✅ |
| agent-context/backend-context.md | ✅ |
| agent-context/test-context.md | ✅ |
| agent-context/product-review-context.md | ✅ |

## 5. 结论

生成文档完整，内容可追溯，待确认问题已保留。
