# 产出示例

假设 PMContext 已存在「会员体系重构」，给 AI 的 PRD 片段：

```markdown
## Agent Context
- 技术栈: Node.js 18 + PostgreSQL 15 + Redis 7
- 目录结构: src/modules/membership/ (待新建)
- 关键模块: src/modules/payment/ (复用现有支付模块)

## 用户故事
🎯 US-1: 会员升级
- 规则: 升级后立即生效，差价按剩余天数按比例计算
- 验收: 升级响应 < 500ms，差额精度到分
← PMContext: 概述/价值验证度量

## [待确认] 年付折扣比例
- 隔离区: 不进入用户故事，待 PM 确认后补入
```

# 延伸参考

- [Anthropic Agent Skills 规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [AI PRD vs Human PRD 的差异设计](https://www.productcompass.pm/p/what-exactly-is-product-discovery)

# 实战提示

- **可执行规则用祈使句**：「升级后立即生效」而非「系统应该支持升级」
- **[待确认] 项必须进隔离区**：不能混入用户故事，否则 Agent 会臆造实现
- **每条规则配验收标准**：没有验收的规则等于没写，Agent 无从验证
- **Agent Context 要具体到目录路径**：让 Agent 知道在哪写代码
