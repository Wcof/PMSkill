# Generate 模块指南

## 做什么

基于精炼与关联结果，生成可执行、可追溯的 PRD 文档与 Agent 上下文。

## 输入

- `docs/prd-helper/02-refine/`
- `docs/prd-helper/03-relate/`

## 输出

输出到 `docs/prd-helper/04-generate/`：

- `overview/project-overview.md`
- `pages/*.md`
- `rules/*.md`
- `data/*.md`
- `acceptance/*.md`
- `agent-context/*.md`
- `check.md`

## 验收条件

- 不凭空新增业务规则
- 保留待确认问题
- 页面/规则/数据/验收结构完整
- 生成前后可追溯
- 输出 `check.md`
