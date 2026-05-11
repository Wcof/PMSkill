# PRD Helper Skill - Claude Code 安装说明

## Step 0：推荐安装方式（skills@latest）

推荐使用 `skills@latest` 安装到 Claude Code，并选择全部 `prd-*` Skill：

```bash
npx skills@latest add Wcof/PRDContextEngine --agent claude-code --all --full-depth
```

安装完成后，Claude Code 应能加载完整 `/prd-*` 指令。可先运行：

```text
/prd-helper
```

`/prd-helper` 会初始化当前项目，并修复项目级直出命令：

```text
/prd-helper
/prd-start
/prd-stop
/prd-status
/prd-scan
/prd-import
/prd-refine
/prd-relate
/prd-generate
/prd-discuss
/prd-remove
```

## Claude Code Plugin 安装（可选）

如果你希望安装后 `/` 菜单立刻出现插件命令，也可以使用 Claude Code Plugin：

```bash
claude plugin marketplace add Wcof/PRDContextEngine --scope user
claude plugin install prd-helper@prd-helper --scope project
```

然后运行插件入口：

```text
/prd-helper:prd-helper
```

也可以运行 skills.sh 交互安装器（installer）：

```bash
npx skills@latest add Wcof/PRDContextEngine --full-depth
```

选择全部 `prd-*` Skill，并选择 Claude Code 作为安装目标。`prd-helper` 承载四阶段业务规则，其它 `prd-*` Skill 是命令包装。

交互选择时：

- 使用 `↑` / `↓` 移动
- 使用 `Space` 勾选或取消
- 使用 `Enter` 确认
- 不需要输入数字

安装完成后可直接运行：

```text
/prd-helper
```

运行 `/prd-helper` 会自动初始化或修复当前项目：创建 `docs/prd-helper/`、写入 `CLAUDE.md` 配置块，修复 `.claude/commands/prd-helper.md`、`.claude/commands/prd-start.md`、`.claude/commands/prd-status.md` 等真实斜杠命令文件。即使 `docs/prd-helper/` 已存在，也要允许 `/prd-helper` 再次执行，用来补齐缺失的命令文件。采集 hooks 不在初始化时常驻；它们由 `/prd-start` 启用，由 `/prd-stop` 清理。

如果 Claude Code 的 `/` 菜单没有显示完整 `/prd-*`，先确认安装时选择了全部 Skill，或直接使用推荐的非交互命令：

```bash
npx skills@latest add Wcof/PRDContextEngine --agent claude-code --all --full-depth
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

先发送 `/prd-start`，它会自动初始化并开启采集；再确认 `.claude/commands/prd-helper.md` 和 `.claude/commands/prd-start.md` 已生成。`/prd-start` 后可用 `/hooks` 查看 `UserPromptSubmit` 和 `Stop` 是否已有 PRD Helper hook；发送 `/prd-stop` 后，这些 hook 应被清理。

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
