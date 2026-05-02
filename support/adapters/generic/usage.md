# PRD Helper Skill - 通用使用说明

适用于不支持标准 Skills 的 Agent 工具，可复制 Markdown 指令使用。

## 使用方式

如果 Agent 支持标准 Skills，默认先完整安装：

```bash
npx skills@latest add Wcof/PRDContextEngine
```

在安装器（installer）中选择 `prd-helper`，再选择要安装到哪些编码 Agent（coding agents）。安装后运行：

```text
/prd-setup
```

`/prd-setup` 会确认文档保存目录（docs root）、启用 Agent 和采集策略。交互选择时使用 `↑` / `↓` 移动，使用 `Space` 勾选或取消，使用 `Enter` 确认，不需要输入数字。

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
