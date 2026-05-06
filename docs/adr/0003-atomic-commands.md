# ADR 0003: `/prd-helper` 初始化后生成原子指令

## Status

Accepted (updated 2026-05-06)

## Context

早期命令体系采用 `/prd-helper` 作为总入口，通过 `/prd-helper start`、`/prd-helper status` 等子动作分发到具体脚本。后来尝试将初始化入口改为 `/prd-init`，但 `skills@latest` 只会把根 `SKILL.md` 注册成一个 Skill 命令，导致安装后仍只显示 `/prd-helper`。

这种设计导致：
- `/prd-init` 写在文档里，但安装后不会自动出现在 Claude Code 指令列表中
- 用户看到 `/prd-helper` 后，不清楚它是否应该用于初始化
- `/prd-helper <action>` 子动作仍然有包装感，和原子命令目标不一致

## Decision

保留 `prd-helper` 作为唯一安装器可见入口，并明确它只负责初始化。初始化完成后，脚本生成后续原子命令文件。

命令集合（2026-05-06 更新）：
- `/prd-helper` — 初始化项目，由安装器注册
- `/prd-start` — 开启采集（支持 session 续接），由初始化脚本生成
- `/prd-stop` — 停止采集（提示可用 /prd-refine 精炼），由初始化脚本生成
- `/prd-status` — 查看状态，由初始化脚本生成
- `/prd-scan` — 扫描所有 AI 工具 session，由初始化脚本生成
- `/prd-import` — 导入第三方文件夹数据，由初始化脚本生成
- `/prd-refine` — 直接精炼（不强制前置步骤），由初始化脚本生成
- `/prd-relate` — 直接关联（不强制前置步骤），由初始化脚本生成
- `/prd-generate` — 直接生成（不强制前置步骤），由初始化脚本生成
- `/prd-discuss` — 需求研讨模式（原 /prd-grill），由初始化脚本生成
- `/prd-remove` — 卸载，由初始化脚本生成

移除 `/prd-init` 和所有 `/prd-helper <action>` 兼容入口。

### 2026-05-06 变更

1. **删除 `/prd-pause` 和 `/prd-resume`**：功能合并到 start/stop，减少认知负担
2. **新增独立模块指令**：`/prd-refine`、`/prd-relate`、`/prd-generate` 可单独使用，不强制前置步骤
3. **新增 `/prd-import`**：支持导入第三方文件夹数据作为被动材料
4. **重命名 `/prd-grill` → `/prd-discuss`**：更直观的命名
5. **Session 续接**：stop 后再 start 时复用同一 session
6. **Check 脚本报告模式**：无数据时不阻断，有数据时检查错误

## Consequences

- 安装后只看到 `/prd-helper` 是预期行为
- 首次运行 `/prd-helper` 后，Claude Code 项目生成后续命令文件
- 旧的 `/prd-init.md` 和 `/prd-setup.md` 作为遗留命令由卸载脚本清理
- 用户可能需要开启新会话或刷新 Claude Code 命令列表，才能看到刚生成的命令
- 四个业务模块（Collect/Refine/Relate/Generate）各有独立指令，可从任意步骤开始
- Check 脚本改为报告模式，支持跳过前置步骤
