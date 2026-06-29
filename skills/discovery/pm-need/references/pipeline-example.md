# 一键全链路产出示例与实战提示

## 完整链路产出

假设 `$ARGUMENTS = "会员体系重构"`，`--auto` 模式：

### collect 阶段
```
收集了 8 条材料（来源：URL 2 条 / 对话 1 条 / 项目深扫描 4 条（docs/3 个、git/5 条、标记/2 处、配置/1 个） / 知识库 1 条）
```

### refine 阶段
```
8 维推断完成：事实 12 项 / [假设] 5 项 / [待确认] 2 项 / [冲突] 1 项
置信度分布：事实 60% / [假设] 25% / [待确认] 10% / [冲突] 5%
```

### premortem 阶段（--auto 强制编入）
```
Tiger 3 个（Launch-Blocking 1 / Fast-Follow 1 / Track 1）
Paper Tiger 2 个 / Elephant 1 个
假设升级为 Tiger: 1 条（[假设] iOS push 送达率 > 80%，置信度 4）
```

### PMContext 产物（`docs/pm-context/pm-context.md`）
```markdown
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
## 用户登录
### 事实
- 用户需登录才能访问仪表盘 ← 来源: 项目扫描, 审计: <[README+步骤1问题重构] → [/pm-refine 8维之"用户场景"] → [同义词推导: "账号"→Customer] → 事实>
### 规则
- 到期前 7 天发 push 提醒 ← 来源: 用户反馈, 审计: <[材料M1+M2] → [/pm-refine 8维之"优先级"] → [Opportunity Score: 0.9×(1-0.3)=0.63] → 规则>
## 决策日志
| 决策点 | 选项A | 选项B | 最终选择 | 理由 | 来源 | 依据源数 | 工具名摘要 |
|--------|------|------|---------|------|------|---------|-----------|
| 选择认证方案 | JWT | Session | JWT | 无状态+易扩展 | 项目扫描 | 3 | /pm-refine 8维之"技术约束" |
```

### PRD 产物
- **AI PRD**（`prd/ai-prd.md`）：Agent Context + 7 条可执行规则 + 2 个用户故事 + 验收标准含边界场景
- **Human PRD**（`prd/human-prd.md`）：决策理由表 + "为什么现在做"背景 + 追溯清单

### 草图产物
- **HTML 原型**（`sketch/prototype.html`）：会员中心 + 付费方案对比 + 续费流程交互
- **Mermaid 草图**：wireframe.md / ia.md / state.md / flow.md

### 一站式报告
```markdown
## PMSkill 自动完成报告

### 链路用时
- collect: 4 个来源，8 个材料
- refine: 8 个推断维度
- premortem: 3 个 Tiger / 2 个 Paper Tiger / 1 个 Elephant
- PRD: ai-prd.md + human-prd.md
- 原型: prototype.html + 4 个 Mermaid 草图

### 置信度
- 事实: 60%
- [假设]: 25%
- [待确认]: 10%
- [冲突]: 5%
```

## 实战提示

| 场景 | 推荐命令 |
|------|---------|
| 一键全链路 | `/pm-need <需求> --auto` |
| 先调研再决定 | `/pm-need --collect-only` → 看材料 → `/pm-need --refine-only` |
| 增量更新 | `/pm-need --incremental`（不清空 .loop/，不覆盖旧事实） |
| 审计入口 | 一站式报告中的置信度分布：[待确认] > 30% 建议 PM 先审 |
| 只出 PRD | `/pm-prd --auto` |
| 只出草图 | `/pm-sketch --prototype` |

## 延伸参考

- [PM Compass - Product Discovery Guide](https://www.productcompass.pm/p/what-exactly-is-product-discovery)
- [Continuous Discovery Habits - Teresa Torres](https://www.productcompass.pm/p/cpdm)
- [Opportunity Solution Tree Framework](https://www.productcompass.pm/p/the-extended-opportunity-solution-tree)
