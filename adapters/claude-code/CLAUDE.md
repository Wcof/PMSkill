# PRD Helper Skill - Claude Code Instructions

## 项目说明

本项目使用 PRD Helper Skill Kit 处理产品上下文。

## 核心规则

1. **本项目产品上下文处理必须走 prd-helper skill。**
2. **不允许直接从原始材料生成最终 PRD。**
3. **必须区分事实、推断、冲突、待确认。**
4. **必须运行检查。**
5. **必须输出 Context Delta。**

## 工作流程

处理产品上下文时，必须按以下顺序执行：

1. **Collect（采集）**：保存原始上下文到 `docs/prd-helper/01-collect/`
2. **Refine（精炼）**：提取事实、背景、目标、决策、约束、冲突、问题到 `docs/prd-helper/02-refine/`
3. **Relate（关联）**：建立关系到 `docs/prd-helper/03-relate/`
4. **Generate（生成）**：输出文档到 `docs/prd-helper/04-generate/`
5. **Final Check（最终检查，不是第五个业务环节）**：每步都输出 `check.md`，最终输出到 `docs/prd-helper/05-check/`

**重要：不能直接从原始材料生成最终 PRD，必须保留 collect/refine/relate/generate 中间产物。**

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
- `skills/prd-helper/references/collect.md`
- `skills/prd-helper/references/refine.md`
- `skills/prd-helper/references/relate.md`
- `skills/prd-helper/references/generate.md`
- `skills/prd-helper/references/check-rules.md`
- `skills/prd-helper/references/context-delta.md`

## 模板

使用 `skills/prd-helper/assets/templates/` 下的模板文件。
