# PRD Helper Skill - Trae Project Rules

## 项目说明

本项目使用 PRD Helper Skill Kit 处理产品上下文。

## 核心规则

1. 遇到产品需求整理任务时，使用 PRD Helper Skill 流程。
2. 必须按 collect、refine、relate、generate 执行，检查贯穿四环节。
3. 必须保存原始材料。
4. 必须输出 Context Delta。
5. 不允许把 AI 推断当成确定事实。
6. 不能直接从原始材料生成最终 PRD，必须保留中间产物。

## 工作流程

处理产品上下文时，必须按以下顺序执行：

1. **Collect（采集）**：保存原始上下文到 `docs/prd-helper/01-collect/`
2. **Refine（精炼）**：提取事实、背景、目标、决策、约束、冲突、问题到 `docs/prd-helper/02-refine/`
3. **Relate（关联）**：建立关系到 `docs/prd-helper/03-relate/`
4. **Generate（生成）**：输出文档到 `docs/prd-helper/04-generate/`
5. **Check（检查）**：每步都输出 `check.md`，最终输出到 `docs/prd-helper/05-check/`

## 检查要求

每一步完成后都必须运行检查：

- 采集后：`01-collect/check.md`
- 精炼后：`02-refine/check.md`
- 关联后：`03-relate/check.md`
- 生成后：`04-generate/check.md`
- 最终：`05-check/` 下的所有检查文件

## Context Delta

每次完成任务后，必须在 `docs/prd-helper/05-check/context-delta.md` 输出本轮上下文增量。

## 参考文件

详细规则请参考：

- `skills/prd-helper/SKILL.md`
- `skills/prd-helper/references/workflow.md`
- `skills/prd-helper/references/check-rules.md`

## 模板

使用 `skills/prd-helper/assets/templates/` 下的模板文件。
