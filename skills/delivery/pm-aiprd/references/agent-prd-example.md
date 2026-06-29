# 给 AI 的 PRD 产出示例与可执行规则书写技巧

## 完整片段

假设 PMContext 已存在「会员体系重构」，给 AI 的 PRD：

```markdown
# 会员体系重构 AI PRD

## 概述（Overview）
将会员订阅从纯月付扩展为月付+年付双方案，提升续费率和 LTV。

## Agent Context
### 技术栈与约束
- Node.js 18 + PostgreSQL 15 + Redis 7
- M1 Mac 8G 内存：单进程 RSS < 6G（留 2G 给 OS）
- API 延迟 p99 < 200ms
### 目录结构约定
- src/modules/membership/ （待新建）
- src/modules/payment/ （复用现有支付模块）
### 关键模块位置
- PaymentService: src/modules/payment/service.ts
- NotificationService: src/modules/notification/service.ts

## 用户故事（User Stories）
1. As a 月付会员, I want to upgrade to 年付, so that 节省费用并获得连续服务保障
   ← PMContext: 概述/问题与目标 | 审计: 依据源3 + /pm-refine 8维之"用户场景"

2. As a 到期会员, I want to 收到续费提醒, so that 不会因忘记续费而中断服务
   ← PMContext: 概述/现状平替与摩擦力 | 审计: 依据源2 + /pm-refine 8维之"边界条件"

## 实施规则（Rules）
- R-1: 年付价格必须 ≤ 月付 × 10（否则无价格优势）
  ← PMContext: 支付流程/规则 | 审计: 依据源2 + /pm-refine 8维之"优先级"
- R-2: 升级后立即生效，差价按剩余天数比例计算，精度到分
  ← PMContext: 用户登录/规则 | 审计: 依据源1 + /pm-refine 8维之"边界条件"
- R-3: 到期前 7 天发 push 提醒，iOS 端追加短信通道
  ← PMContext: 概述/现状平替与摩擦力 | 审计: 依据源2 + /pm-refine 8维之"价值验证度量"

## 数据模型（Data）
- MemberPlan: { id, userId, type: 'monthly'|'annual', startDate, endDate, autoRenew }
- PaymentRecord: { id, memberId, amount, method, status, createdAt }

## 验收标准（Acceptance）
### US-1: 年付方案选择
- **目标**：月付用户可无缝切换年付
- **前置条件**：用户已登录且当前为月付会员
- **步骤**：
  1. 用户进入会员中心
  2. 点击"升级年付"按钮
  3. 确认差价金额
  4. 完成支付
- **预期结果**：会员类型立即变为年付，到期日延长至 12 个月后
- **边界场景**：支付失败 → 保留月付状态 + 提示重试

## 风险项（Risks）
- ⚠️ [假设] 年付折扣比例未定（置信度 6/10）→ 待 PM 确认后补入 R-1
- ⚠️ [待确认] iOS push 送达率是否 > 80% → 若否，短信通道为必选非备选

## 超出范围（Out of Scope）
- 会员等级体系重构（本次只做付费周期扩展）
- 多币种支持（Phase 2）
```

## 可执行规则书写技巧

| 技巧 | 正确 ✅ | 错误 ❌ |
|------|---------|---------|
| 用祈使句 | 「升级后立即生效」 | 「系统应该支持升级」 |
| 有具体参数 | 「到期前 7 天发提醒」 | 「提前发提醒」 |
| 可验证 | 「差价精度到分」 | 「差价计算准确」 |
| 标注来源 | `← PMContext: 支付流程/规则` | 无来源标注 |

## [待确认] 项处理

| 占比 | 处理 |
|------|------|
| ≤ 30% | 写入风险项章节，标"待 PM 确认"，不进入用户故事 |
| 30%-50% | 同上 + 顶部加 🟡 警示"PRD 草案" |
| > 50% | 顶部加 🔴"PRD 不可执行" |

## 延伸参考

- [AI PRD Template - Miqdad Jaffer (OpenAI)](https://www.productcompass.pm/p/ai-prd-template)
- [Anthropic Agent Skills 规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
