# Checks 指南

`checks/` 是横向质量门禁，不是第五业务模块。

## 覆盖范围

- collect 后检查
- refine 后检查
- relate 后检查
- generate 后检查
- 最终总检查

## 检查产物位置

检查产物统一输出到目标项目 `docs/prd-helper/` 各阶段目录与 `05-check/`。

- `01-collect/check.md`
- `02-refine/check.md`
- `03-relate/check.md`
- `04-generate/check.md`
- `05-check/full-check.md`
- `05-check/gap-check.md`
- `05-check/relation-check.md`
- `05-check/source-check.md`
- `05-check/generated-check.md`
- `05-check/context-delta.md`

## 模板

- `checks/templates/05-final-check-template.md`
- `checks/templates/05-context-delta-template.md`
