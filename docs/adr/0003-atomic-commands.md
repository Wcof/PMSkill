# ADR 0003: 原子指令模式替代包装命令

## Status

Accepted

## Context

早期命令体系采用 `/prd-helper` 作为总入口，通过 `/prd-helper start`、`/prd-helper status` 等子动作分发到具体脚本。部分平台（如 Codex、Trae）只显示一个 `/prd-helper` 命令，用户必须用兼容入口 `/prd-helper start` 来执行采集操作。

这种设计导致：
- 用户看到的是一个命令，实际要靠参数分发，认知负担高
- 安装器生成的命令文件包含"兼容入口"文案，文档和提示不一致
- `/prd-helper` 既是 Skill 名又是命令入口，职责混淆

## Decision

改为原子指令模式：每个斜杠命令对应 Skill 生命周期的一个离散状态操作。

命令集合：
- `/prd-init` — 初始化项目
- `/prd-start` — 开启采集
- `/prd-pause` — 暂停采集
- `/prd-resume` — 恢复采集
- `/prd-stop` — 停止采集
- `/prd-status` — 查看状态
- `/prd-remove` — 卸载

移除所有 `/prd-helper <action>` 兼容入口。Skill 名称仍保留 `prd-helper`，与命令命名解耦。

## Consequences

- `/prd-start` 等采集命令保留自动初始化逻辑：未初始化时先执行 setup 脚本，再执行本命令操作
- `/prd-init` 和 `/prd-remove` 不包含自动初始化检查，直接执行
- 旧会话输入 `/prd-helper` 将不再有兼容提示，用户需改用原子指令
- 用户需重新安装 Skill 获取新版本命令文件
