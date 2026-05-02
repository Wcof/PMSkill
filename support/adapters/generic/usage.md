# PRD Helper Skill - 通用使用说明

适用于不支持标准 Skills 的 Agent 工具，可复制 Markdown 指令使用。

## 使用方式

如果 Agent 支持标准 Skills，默认先完整安装：

```bash
npx skills@latest add Wcof/PRDContextEngine --all
```

如果需要手动选择 Agent，也可以运行 `npx skills@latest add Wcof/PRDContextEngine`。安装后运行：

```text
/prd-init
```

首次运行 `/prd-init` 会自动初始化项目，创建 `docs/prd-helper/` 并写入 Agent 配置文件。Claude Code 项目还会生成 `.claude/commands/prd-start.md` 等真实斜杠命令文件。

卸载当前项目中的 PRD Helper：

```text
/prd-remove
```

Agent 收到该指令后，执行安装目录中的卸载脚本：

```bash
python3 .agents/skills/prd-helper/scripts/remove-prd-helper.py --project .
```

如果当初是全局安装：

```bash
npx skills@latest remove prd-helper --agent '*' --global -y
```

交互式卸载可以运行 `npx skills@latest remove`。

完整卸载分两层：卸载脚本先清理 Agent 配置文件中的 PRD Helper 引用，再调用 `skills remove` 删除 Skill 安装目录。

如果 Agent 不支持标准 Skills，将以下指令复制到你的 Agent 对话中，然后提供原始材料即可。

---

## 指令开始

你是一个产品上下文处理助手。请按照 `support/adapters/canonical-rules.md` 中的规则处理我提供的产品材料。

核心流程：Collect → Refine → Relate → Generate → Final Check

关键规则、采集命令和检查要求统一见 `support/adapters/canonical-rules.md`。

---

## 指令结束

## 参考文件

- `support/adapters/canonical-rules.md` — 完整规则
- `SKILL.md` — 流程编排
- `modules/*/guide.md` — 各模块行为约束
