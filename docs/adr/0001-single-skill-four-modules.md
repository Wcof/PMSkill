# ADR 0001: Single Skill With Four Business Modules

## Status

Accepted

## Context

PRD Helper 需要支持类似 `npx skills@latest add Wcof/PRDContextEngine` 的安装器（installer）体验：用户在安装器中选择 `prd-helper` 和目标编码 Agent（coding agents），然后在 Agent 中运行 `/prd-helper` 完成项目初始化。项目内部有 Collect、Refine、Relate、Generate 四个业务模块，但它们属于同一个 Skill。

## Decision

仓库采用单 Skill 架构：

- 根目录 `SKILL.md` 是唯一 Skill 入口。
- `modules/collect`、`modules/refine`、`modules/relate`、`modules/generate` 是同一个 Skill 内部模块。
- `checks/` 是横向质量门禁，不作为第五个业务模块。
- 不使用 `skills/prd-helper/SKILL.md` 的 Skill collection 结构。
- Step 0 是通过安装器（installer）安装完整 `prd-helper` Skill，再运行 `/prd-helper`，不按业务模块拆分安装。

## Consequences

- 默认安装命令：`npx skills@latest add Wcof/PRDContextEngine`。
- 安装后必须运行 `/prd-helper`，由 Agent 执行初始化脚本创建项目结构。
- 完整卸载通过 `/prd-remove` 触发；Agent 执行 `remove-prd-helper.py`，先清理 Agent 配置引用，再调用 `npx skills@latest remove prd-helper ...`。
- 模块可以共享 `scripts/lib/` 中的工具。
- 文档、适配器、检查脚本必须避免把 Collect 或其它模块描述成独立 Skill。
