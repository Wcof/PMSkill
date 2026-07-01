# 优先级框架参考

> 由 `/pm-refine` 的 P1 维度 4「优先级」推断时参考。详见 `SKILL.md` 的「PM 自检维度（8 维全覆盖）」节。

## 核心原则

**优先排问题（机会），不是排方案。** 先选框架确定哪些用户问题最值得解决，再想解决方案。

## ICE 框架

适合快速打分，用户规模差异小时用。

- **I**（Impact）= Opportunity Score × 用户数。先算问题对单个用户的价值，再乘用户规模
- **C**（Confidence）= 把握度(1-10)，对 Impact 估计的信心
- **E**（Ease）= 实现难度倒数(1-10)，10 = 最容易

**Score = I × C × E**。越高越优先。

## RICE 框架

用户规模差异大时用，将 ICE 的 Impact 拆为 Reach 和 Impact 两因子。

- **R**（Reach）= 影响的用户数
- **I**（Impact）= 每个用户的价值（Opportunity Score）
- **C**（Confidence）= 把握度(0-100%)，细于 ICE 的 1-10
- **E**（Effort）= 人月数，因子在分母

**Score = (R × I × C) / E**

## Opportunity Score（推荐）

Dan Olsen（*The Lean Product Playbook*）。调查用户对每个需求的**重要性**和**满意度**（归一化到 0-1）。

- **Current Value** = Importance × Satisfaction
- **Opportunity Score** = Importance × (1 − Satisfaction)
- **Customer Value Created** = Importance × (S2 − S1)，S1=前满意度，S2=后满意度

高重要性 + 低满意度 = 最优机会。画在 Importance vs Satisfaction 图上，左上象限是 sweet spot。

## Kano Model

判断功能类型，必备优先、兴奋做差异化。

| 类型 | 用户感受 | 优先级原则 |
|------|---------|-----------|
| 必备（Must-be） | 没它会不满，有它不惊喜 | 不做就不上线 |
| 期望（Performance） | 越多越满意 | 做更多更好 |
| 兴奋（Attractive） | 没有无所谓，有了惊喜 | 差异化竞争用 |
| 无差异（Indifferent） | 有没有都一样 | 删 |
| 反向（Reverse） | 有了反而不满 | 不做 |

## MoSCoW

用于 MVP 边界划定，不适合做精细优先级排序（源自项目管理）。

- **Must**：不做就不上线
- **Should**：重要但不紧急，可稍后
- **Could**：nice-to-have，有余力再做
- **Won't**：明确排除

## Weighted Decision Matrix

多因子加权评分，用于干系人达成共识的场景。

1. 确定评价因子（如：用户影响、商业价值、实现成本）
2. 给每个因子赋权重
3. 对每个方案在各因子上打分
4. 加权求和，按总分排序

## Opportunity Solution Tree（Teresa Torres）

将优先级推断结构化为四层树，**防止跳方案**：

```
Desired Outcome（上面一个指标）
  → Opportunities（第二层：3-7个用户机会，用 Opportunity Score 排序）
    → Solutions（第三层：Top 2-3 机会各发散 ≥3 个方案，Product Trio 协作）
      → Experiments（底层：最可行方案的快速验证实验）
```

关键纪律：不允许只产出一个方案就进入权衡。

## 所选框架的记录

选定框架后，在 PMContext 的决策日志中记录：
```markdown
| 决策点 | 选项A | 选项B | 最终选择 | 理由 | 来源 | 依据源数 | 工具名摘要 |
|--------|------|------|---------|------|------|---------|-----------|
```