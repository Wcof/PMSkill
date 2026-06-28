# 产出示例

Pre-Mortem 输出片段：

```markdown
## 假设：上线 14 天后，会员续费率不升反降

### 倒推原因
1. 年付折扣太低，用户算账不划算 → Tiger
2. 续费提醒 UI 被 SPAM 过滤 → Paper Tiger (已有邮件白名单)
3. 数据迁移遗漏历史会员等级 → Elephant (Q4 再处理)

## Tiger 行动计划
| 风险 | 负责人 |截止日期 | 行动 |
|------|--------|---------|------|
| 折扣太低 | PM | 7/15 | 跑 LTV 测算定折扣 |
```

# 延伸参考

- [Pre-Mortem 原始方法 - Gary Klein](https://www.productcompass.pm/p/what-exactly-is-product-discovery)
- [Risk Matrix 最佳实践](https://www.productcompass.pm/p/cpdm)

# 实战提示

- **假设「已失败」再倒推**：不要列「可能的风险」，要从失败结果反推原因
- **Tiger 必须有负责人+日期**：无负责人的风险等于没处理
- **Paper Tiger 要说明「为何不是真风险」**：否则团队会误判优先级
- **低置信度假设最可能升级为 Tiger**：交叉检查 PMContext 的 [假设] 项
