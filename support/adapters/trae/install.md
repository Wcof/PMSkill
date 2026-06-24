# Trae 安装说明

## Step 0：默认完整安装

推荐使用免交互安装，避免安装器英文提示干扰：

```bash
npx skills@latest add Wcof/PMSkill --all
```

也可以运行 skills.sh 交互安装器（installer）：

```bash
npx skills@latest add Wcof/PMSkill
```

选择全部 `prd-*` Skill，并选择 Trae 或 Trae CN 作为安装目标。`prd-helper` 承载四阶段业务规则，其它 `prd-*` Skill 是命令包装。

交互选择时：

- 使用 `↑` / `↓` 移动
- 使用 `Space` 勾选或取消
- 使用 `Enter` 确认
- 不需要输入数字

安装完成后，在 Trae 中可直接运行：

```text
/prd-helper
```

首次运行任意 `/prd-*` 会自动初始化项目：创建 `docs/prd-helper/`，并写入 Trae `project_rules.md` 配置块。

## 卸载

在 Trae 对话中发送：

```text
/prd-remove
```

Agent 会清理 Trae `project_rules.md` 中的 PRD Helper 配置块，然后从当前项目卸载 Trae 中的 PRD Helper Skill。

如果需要手动执行同等命令：

```bash
python3 .trae/skills/prd-helper/scripts/remove-prd-helper.py --agent trae --project .
```

如果使用 Trae CN：

```bash
python3 .trae/skills/prd-helper/scripts/remove-prd-helper.py --agent trae-cn --project .
```

如果当初是全局安装：

```bash
npx skills@latest remove prd-helper --agent trae --global -y
```

交互式卸载：

```bash
npx skills@latest remove
```

卸载 Skill 不会自动删除 `docs/prd-helper/` 中已经生成的 PRD 文档。

## 手动安装步骤（备选）

1. 将本仓库复制到目标项目中（路径按 Trae 当前版本调整）：

```bash
cp -r /path/to/PMSkill /path/to/your-project/repository root
```

2. 将 `support/adapters/trae/project_rules.md` 的内容添加到 Trae 的项目规则中。

## 验证安装

安装完成后，目标项目结构应如下：

```
your-project/
├── skills/
│   └── prd-helper/
│       ├── SKILL.md
│       ├── modules/
│       ├── checks/
│       └── scripts/
└── docs/
    └── prd-helper/                    # 生成的 PRD 文档
        ├── 01-collect/
        ├── 02-refine/
        ├── 03-relate/
        ├── 04-generate/
        └── 05-check/
```

## 使用方式

安装后，先发送 `/prd-start` 自动初始化并开始主动采集：

```text
/prd-start
```

之后向 Trae Agent 提供产品讨论、会议纪要、原型说明等材料，Trae 会按照 project_rules.md 中定义的流程进行处理。

## 注意

Trae 的实际 Skill 文件落点需要在实现时根据当前版本验证。上述安装路径为建议路径。
