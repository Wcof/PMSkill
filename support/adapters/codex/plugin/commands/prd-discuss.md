# /prd-discuss

开启需求研讨模式 — 压力测试产品方案。

## 前置条件

- 必须已执行 `/prd-start`（`capture_mode` 为 `on`）

## 流程

### Phase 1: 扫描与呈现

1. 读取 `{docs_root}/01-collect/active/` 和 `{docs_root}/01-collect/passive/` 下所有文件
2. 梳理矛盾点、模糊术语、未解决的冲突
3. 向用户呈现发现，询问：基于这些矛盾来 battle，还是有新命题？

### Phase 2: 持续 Battle

进入 grill 模式，遵循以下规则：

- 逐个问题追问，等用户回答后再继续
- 每个问题附带推荐答案
- 挑战术语表冲突、精炼模糊语言
- 用具体场景压力测试领域关系
- 交叉引用代码/文档验证用户陈述
- 实时更新项目 `CONTEXT.md`（格式见 `{skill_root}/modules/grill/templates/CONTEXT-FORMAT.md`）
- 谨慎创建 ADR（格式见 `{skill_root}/modules/grill/templates/ADR-FORMAT.md`）

### 结束

生成 `{docs_root}/01-collect/grill/battle-summary.md` 和 `open-questions.md`。
