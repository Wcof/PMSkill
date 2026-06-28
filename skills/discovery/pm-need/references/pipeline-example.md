# 产出示例

假设 `$ARGUMENTS = "会员体系重构"`，完整链路产出：

**PMContext**（`docs/pm-context/pm-context.md`）：
```
# PMContext: 会员体系重构
## 概述
### 问题与目标
- 事实: 当前会员体系仅支持按月订阅，续费率 QoQ 下降 12%（← 对话: 用户反馈）
- [假设: 用户希望有年付选项，7/10]（推断自用户调研中 NPS 评分的关联分析）
- [待确认] 年付用户 LTV 是否显著高于月付（PM 需补充财务数据）
### 现状平替与摩擦力
- 用户目前手动记录到期日，忘记续费后重新开通（← 用户访谈 #3）
### 价值验证度量
- 核心: 年付转化率 ≥ 15% within 30 天
```

**AI PRD**（`docs/pm-context/prd/ai-prd.md`）：含 Agent Context（技术栈 Node.js + PostgreSQL）、可执行规则 7 条、验收标准含边界场景。

**Human PRD**（`docs/pm-context/prd/human-prd.md`）：含决策理由表、"为什么现在做"背景、追溯清单。

**HTML 原型**（`docs/pm-context/sketch/prototype.html`）：会员中心页面 + 付费方案对比 + 续费流程交互。

# 延伸参考

- [PM Compass - Product Discovery Guide](https://www.productcompass.pm/p/what-exactly-is-product-discovery)
- [Continuous Discovery Habits - Teresa Torres](https://www.productcompass.pm/p/cpdm)
- [Opportunity Solution Tree Framework](https://www.productcompass.pm/p/the-extended-opportunity-solution-tree)

# 实战提示

- **`--auto` 是默认姿势**：零确认模式省掉 PM 等待，适合大多数场景
- **`--collect-only` 用于调研阶段**：先扫一圈看有什么材料，再决定要不要 refine
- **增量更新别忘 `--incremental`**：忘了会导致旧 PMContext 被覆盖丢失历史推断
- **一站式报告中的置信度分布是审计入口**：[待确认] > 30% 建议 PM 先审再决策
