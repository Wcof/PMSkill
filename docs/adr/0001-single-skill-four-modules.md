# ADR 0001: One Product Workflow With Command Skill Wrappers

## Status

Superseded by ADR 0004 (2026-06-24). The four-stage pipeline model has been replaced by PMContext as the sole Entity with Skills organized into setup/discovery/delivery/visualization buckets.

## Context

PRD Helper 需要支持 `npx skills@latest add Wcof/PMSkill` 的安装体验。业务上它仍然只有一个产品上下文编译流程，包含 Collect、Refine、Relate、Generate 四个阶段；但安装体验需要把 `/prd-*` 原子指令在安装时暴露出来。

## Decision

仓库采用“一个业务流程，多命令 Skill 包装”的结构：

- `skills/prd-helper/SKILL.md` 承载 PRD Helper 的核心业务规则和四阶段流程。
- `skills/prd-start`、`skills/prd-stop` 等目录是安装器可发现的命令包装，用于注册对应 slash command。
- `modules/collect`、`modules/refine`、`modules/relate`、`modules/generate` 仍是同一个业务流程内部模块，不拆成独立产品实体。
- `checks/` 是横向质量门禁，不作为第五个业务模块。
- `scripts/prd-command-dispatch.py` 是技术分发器，负责首次执行时懒初始化项目并调用对应模块脚本。

## Consequences

- 默认安装命令仍是 `npx skills@latest add Wcof/PMSkill`。
- 安装器应发现完整 `prd-*` Skill 集合；`/prd-helper` 不再是后续命令注册的前置条件。
- 完整卸载通过 `/prd-remove` 触发；Agent 执行 `remove-prd-helper.py`，清理 Agent 配置、项目级兜底命令和 hooks。
- 模块可以共享 `scripts/lib/` 中的工具。
- 文档、适配器、检查脚本必须避免把 Collect 或其它模块描述成独立业务 Skill；命令 Skill 只是安装器包装。
