# Pre-Mortem 产出示例与 Tiger/Paper Tiger/Elephant 技巧

## 完整片段

会员体系重构 Pre-Mortem：

```markdown
# Pre-Mortem: 会员体系重构

## 假设场景
产品上线 14 天后失败。以下是我们认为可能出错的地方。

## Tigers（真风险）
| 风险 | 风险域 | 紧急度 | 缓解措施 | 负责人 | 完成日期 |
|------|--------|--------|---------|--------|---------|
| 年付定价不合理导致 LTV 下降 | Value | Launch-Blocking | 做价格敏感度 A/B 测试 | PM | 上线前 2 周 |
| 续费提醒 push 被 iOS 屏蔽 | Usability | Fast-Follow | 备选短信通道 | 后端 | 上线后 7 天 |
| 订单表迁移导致历史数据丢失 | Feasibility | Launch-Blocking | 数据备份 + 回滚方案 | 后端 | 上线前 |
| M1 Mac 8G 内存跑不动新计算逻辑 | Feasibility | Track | 压测 RSS，超 6G 则拆为异步 | 后端 | 上线前 1 周 |

## Paper Tigers（纸老虎）
| 风险 | 风险域 | 为什么不太可能发生 |
|------|--------|------------------|
| 竞品抄年付方案 | Strategy | 我们的核心壁垒是数据网络效应，非定价模式 |
| 用户反感 push 提醒 | Value | 调研显示 80% 用户希望收到提醒 |

## Elephants（房间里的大象）
| 风险 | 风险域 | 调查方式 |
|------|--------|------------|
| 年付退款政策还没定 | Viability | 上线前必须敲定退款策略 |
| 客服团队没培训年付相关话术 | Team | 协调客服负责人排培训 |

## 行动计划（Launch-Blocking Tigers）
| 风险 | 缓解措施 | 负责人 | 完成日期 |
|------|---------|--------|---------|
| 年付定价不合理 | 价格敏感度 A/B 测试 | PM | 上线前 2 周 |
| 订单表迁移数据丢失 | 全量备份 + 灰度迁移 + 回滚脚本 | 后端 | 上线前 |

## 假设清单交叉检查
| PMContext 假设 | 置信度 | 假设失败后果 | 风险升级 |
|--------------|--------|------------|---------|
| 用户希望有年付选项 | 7/10 | 年付转化率 < 5%，方案失败 | 维持 Track |
| iOS push 送达率 > 80% | 4/10 | 提醒失效，续费率不升 | 升级为 Tiger |
```

## Tiger/Paper Tiger/Elephant 技巧

| 技巧 | 说明 |
|------|------|
| **假设「已失败」再倒推** | 不要列"可能的风险"，要从失败结果反推原因（5-Why 根因分析） |
| **Tiger 必须有负责人+日期** | 无负责人的风险等于没处理 |
| **Tiger ≤ 5 个** | 超出的降级为 Fast-Follow，行动计划过载不可执行 |
| **Paper Tiger 要说明「为何不是真风险」** | 否则团队会误判优先级 |
| **Elephant 是"没人讨论但可能真实"** | 不是"不重要"，是"被忽略" |
| **8 域全覆盖** | Value/Usability/Viability/Feasibility/Ethics/GTM/Strategy/Team，每域至少 1 条 |
| **低置信度假设最可能升级为 Tiger** | 交叉检查 PMContext 的 [假设] 项，置信度 ≤ 5 优先 |

## 延伸参考

- [How Meta and Instagram Use Pre-Mortems](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)
- [How to Manage Risks as a Product Manager](https://www.productcompass.pm/p/how-to-manage-risks-as-a-product-manager)
- [Assumption Prioritization Canvas](https://www.productcompass.pm/p/assumption-prioritization-canvas)
