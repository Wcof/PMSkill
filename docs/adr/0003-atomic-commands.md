# ADR 0003: `/prd-helper` 初始化后生成原子指令

## Status

Accepted

## Context

早期命令体系采用 `/prd-helper` 作为总入口，通过 `/prd-helper start`、`/prd-helper status` 等子动作分发到具体脚本。后来尝试将初始化入口改为 `/prd-init`，但 `skills@latest` 只会把根 `SKILL.md` 注册成一个 Skill 命令，导致安装后仍只显示 `/prd-helper`。

这种设计导致：
- `/prd-init` 写在文档里，但安装后不会自动出现在 Claude Code 指令列表中
- 用户看到 `/prd-helper` 后，不清楚它是否应该用于初始化
- `/prd-helper <action>` 子动作仍然有包装感，和原子命令目标不一致

## Decision

保留 `prd-helper` 作为唯一安装器可见入口，并明确它只负责初始化。初始化完成后，脚本生成后续原子命令文件。

命令集合：
- `/prd-helper` — 初始化项目，由安装器注册
- `/prd-start` — 开启采集，由初始化脚本生成
- `/prd-pause` — 暂停采集，由初始化脚本生成
- `/prd-resume` — 恢复采集，由初始化脚本生成
- `/prd-stop` — 停止采集，由初始化脚本生成
- `/prd-status` — 查看状态，由初始化脚本生成
- `/prd-remove` — 卸载，由初始化脚本生成

移除 `/prd-init` 和所有 `/prd-helper <action>` 兼容入口。

## Consequences

- 安装后只看到 `/prd-helper` 是预期行为
- 首次运行 `/prd-helper` 后，Claude Code 项目生成 `/prd-start`、`/prd-status` 等命令文件
- 旧的 `/prd-init.md` 和 `/prd-setup.md` 作为遗留命令由卸载脚本清理
- 用户可能需要开启新会话或刷新 Claude Code 命令列表，才能看到刚生成的命令
