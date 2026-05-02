# PRD Helper Skill - Claude Code 安装说明

## Step 0：默认完整安装

推荐使用免交互安装，避免安装器英文提示干扰：

```bash
npx skills@latest add Wcof/PRDContextEngine --all
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

安装完成后，在 Claude Code 中运行：

```text
/prd-helper
```

首次运行 `/prd-helper` 会自动初始化项目：创建 `docs/prd-helper/`、写入 `CLAUDE.md` 配置块，并生成 `.claude/commands/prd-start.md`、`.claude/commands/prd-status.md` 等真实斜杠命令文件。

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

先发送 `/prd-helper` 完成自动初始化，再发送 `/prd-start`。如果 Claude Code 创建了 `docs/prd-helper/01-collect/` 目录并生成 `.claude/commands/prd-start.md`，说明安装成功。

## 使用

1. 发送 `/prd-start` 开启采集
2. 提供产品材料（会议纪要、原型说明、客户反馈等）
3. 发送 `/prd-stop` 停止采集
4. Agent 自动执行 Refine → Relate → Generate 流程

如果当前会话暂时没有刷新出 `/prd-start`，可以使用兼容入口：

```text
/prd-helper start
```

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
