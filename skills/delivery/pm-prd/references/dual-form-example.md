# 产出示例

`/pm-prd 会员体系重构`（自动模式）链路：

```
1. 读取 docs/pm-context/pm-context.md ✓
2. 调用 /pm-aiprd → 生成 ai-prd.md (7 用户故事, 12 规则)
3. 调用 /pm-humanprd → 生成 human-prd.md (5 决策理由)
4. 审计摘要: 未覆盖风险项 2 条 [待确认]
5. 🔴 CHECKPOINT 等用户确认
```

# 延伸参考

- [PM Compass - PRD 双形态策略](https://www.productcompass.pm/p/what-exactly-is-product-discovery)
- [Anthropic Agent Skills 规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

# 实战提示

- **`--auto` 跳过审计门**：适合原型快速迭代，正式交付前建议手动审计一轮
- **`--skip-human` 只出 AI 版**：内部技术评审时用，省去决策理由叙事
- **审计摘要必看未覆盖风险项**：这些是 PMContext 中 [待确认] 但 PRD 未处理的项
- **双形态必须同源**：ai-prd 和 human-prd 引用同一 PMContext，差异只在写法
