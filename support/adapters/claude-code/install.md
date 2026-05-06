# PRD Helper Skill - Claude Code 安装说明

## Step 0：推荐安装方式（Claude Code Plugin）

如果希望安装后 Claude Code 的 `/` 菜单直接出现 PRD Helper 入口，使用 Claude Code Plugin：

```bash
claude plugin marketplace add Wcof/PRDContextEngine --scope user
claude plugin install prd-helper@prd-helper --scope project
```

安装完成后，在 Claude Code 中运行插件入口：

```text
/prd-helper:prd-helper
```

它会初始化当前项目，并生成项目级直出命令：

```text
/prd-helper
/prd-start
/prd-pause
/prd-resume
/prd-stop
/prd-status
/prd-scan
/prd-remove
```

## Skill 安装（通用 Agent）

`skills@latest` 只安装 Skill 本体，不会自动执行初始化，也不会直接写入 `.claude/commands/`：

```bash
npx skills@latest add Wcof/PRDContextEngine --agent claude-code --skill prd-helper -y
```

也可以运行 skills.sh 交互安装器（installer）：

```bash
npx skills@latest add Wcof/PRDContextEngine
```

选择 `prd-helper`，并选择 Claude Code 作为安装目标。这个 Skill 内部包含采集、精炼、关联、生成四个模块，不拆分安装。

交互选择时：

- 使用 `↑` / `↓` 移动
- 使用 `Space` 勾选或取消
- 使用 `Enter` 确认
- 不需要输入数字

安装完成后，如果 Claude Code 能显示 Skill 入口，可以运行：

```text
/prd-helper
```

运行 `/prd-helper` 会自动初始化或修复当前项目：创建 `docs/prd-helper/`、写入 `CLAUDE.md` 配置块，生成 `.claude/commands/prd-helper.md`、`.claude/commands/prd-start.md`、`.claude/commands/prd-status.md` 等真实斜杠命令文件。即使 `docs/prd-helper/` 已存在，也要允许 `/prd-helper` 再次执行，用来补齐缺失的命令文件。采集 hooks 不在初始化时常驻；它们由 `/prd-start` 和 `/prd-resume` 启用，由 `/prd-pause` 和 `/prd-stop` 清理。

如果 Claude Code 的 `/` 菜单没有显示 `/prd-helper`，这是 `skills@latest` 与 Claude CLI 命令体系的边界，不是安装脚本已经执行。请改用上面的 Plugin 安装方式，或手动执行：

```bash
python3 .claude/skills/prd-helper/scripts/setup-prd-helper.py --project . --docs-root docs/prd-helper --agent claude-code
```

## 卸载

在 Claude Code 对话中发送：

```text
/prd-remove
```

Agent 会清理 `CLAUDE.md` 中的 PRD Helper 配置块，然后从当前项目卸载 Claude Code 中的 PRD Helper Skill。

如果需要手动执行同等命令：

```bash
python3 .claude/skills/prd-helper/scripts/remove-prd-helper.py --agent claude-code --project .
```

如果当初是全局安装：

```bash
npx skills@latest remove prd-helper --agent claude-code --global -y
```

交互式卸载：

```bash
npx skills@latest remove
```

卸载 Skill 不会自动删除 `docs/prd-helper/` 中已经生成的 PRD 文档。

## 验证安装

先发送 `/prd-helper` 完成自动初始化，再确认 `.claude/commands/prd-helper.md` 和 `.claude/commands/prd-start.md` 已生成，然后重开 Claude Code 会话或刷新命令列表后发送 `/prd-start`。`/prd-start` 后可用 `/hooks` 查看 `UserPromptSubmit` 和 `Stop` 是否已有 PRD Helper hook；发送 `/prd-pause` 或 `/prd-stop` 后，这些 hook 应被清理。

## 使用

1. 发送 `/prd-start` 开启采集
2. 提供产品材料（会议纪要、原型说明、客户反馈等）
3. 发送 `/prd-stop` 停止采集
4. Agent 自动执行 Refine → Relate → Generate 流程

## 手动安装（备选）

如果无法使用 `npx`，可以手动复制：

```bash
# 将仓库克隆到你的 Agent skills 目录
git clone https://github.com/Wcof/PRDContextEngine.git ~/.claude/skills/prd-helper
```

然后在项目的 `CLAUDE.md` 中引用：
```markdown
详细规则请参考 `~/.claude/skills/prd-helper/SKILL.md`
```
