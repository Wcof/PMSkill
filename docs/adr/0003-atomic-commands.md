# ADR 0003: 安装时注册 `/prd-*` 原子指令

## Status

Superseded (2026-06-24). The 11 `prd-*` atomic commands have been replaced by 12 `pm-*` Skills with user-invoked/model-invoked dual-axis invocation model. (updated 2026-05-10)

## Context

早期命令体系采用 `/prd-helper` 作为总入口，通过初始化脚本生成 `/prd-start`、`/prd-status` 等项目级命令。这个方案在 Claude Code 中可以作为兜底，但在 Codex App 等会话里存在刷新问题：用户执行 `/prd-helper` 后，当前 `/` 菜单不一定重新扫描新生成的命令。

`skills@latest` 的事实边界是：它安装 Skill，不执行项目初始化脚本，也没有可依赖的 postinstall hook。并且当仓库根目录存在带 `name` 和 `description` frontmatter 的 `SKILL.md` 时，默认浅扫描会把仓库识别为单一 Skill。

## Decision

PRD Helper 改为多 Skill 命令包：`skills/` 下提供 11 个安装器可发现的 Skill。

- `/prd-helper` — 初始化或修复当前项目配置
- `/prd-start` — 开启采集
- `/prd-stop` — 停止采集
- `/prd-status` — 查看状态
- `/prd-scan` — 扫描所有 AI 工具 session
- `/prd-import` — 导入第三方文件夹数据
- `/prd-refine` — 直接精炼
- `/prd-relate` — 直接关联
- `/prd-generate` — 直接生成，必要时输出 Limited Generate
- `/prd-discuss` — 需求研讨模式
- `/prd-remove` — 卸载

根目录保留 `SKILL.md` 作为本地直接下载/克隆后的自然语言兜底入口，但不包含可安装 Skill frontmatter，避免抢占 `npx skills@latest add Wcof/PMSkill` 的默认发现。`skills/prd-helper/SKILL.md` 承载核心业务规则并携带运行时脚本；其他 `skills/prd-*/SKILL.md` 是轻量命令包装，只调用 `scripts/prd-command-dispatch.py`。

通过 `npx skills@latest add Wcof/PMSkill` 安装完整命令包时，默认即可发现完整命令集合。例如：

```bash
npx skills@latest add Wcof/PMSkill --all
```

`/prd-helper` 不再是后续命令出现的前置条件。任意 `/prd-*` 首次执行时，都通过 dispatcher 懒初始化 `docs/prd-helper/`、Agent 配置、项目级兜底命令和 Hook 配置。

## Consequences

- `npx skills@latest add Wcof/PMSkill` 应能发现完整 `/prd-*` Skill 集合。
- 直接下载仓库并从本地安装时，根 `SKILL.md` 提供稳定入口。
- 项目级 `.claude/commands`、`.codex/commands` 仍会由 setup 脚本补齐，但定位为旧版本或菜单刷新失败时的兜底。
- 多 Skill 包装不是新的领域实体；Collect、Refine、Relate、Generate 的领域模型不变。
- 如果用户只选择安装 `prd-helper`，仍只会看到 `/prd-helper`；文档必须提醒安装全部 `prd-*` Skill。
