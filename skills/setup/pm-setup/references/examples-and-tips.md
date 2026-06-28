# 产出示例

一次典型配置流程：

```
Step 1: 发现 CLAUDE.md 已存在 → 追加 PMSkill 块
Step 2: 用户选 "docs/pm-context/" 为产物目录
Step 3: 用户选 "中文" 为语言
Step 4: 用户跳过了知识库配置
Step 5: 写入后确认

写入到 CLAUDE.md:
## PMSkill
- 产物目录：docs/pm-context/
- 语言：中文
- 知识库：无
```

# 延伸参考

- [AtomCode 多 Agent 配置指南](https://atomcode.dev/docs/agents)
- [PMSkill 架构文档](CONTEXT.md)

# 实战提示

- **运行一次就够了**：`/pm-setup` 是唯一需要手动配置的 skill，后续全自动
- **产物目录不改也行**：`docs/pm-context/` 是大多数项目的最佳选择
