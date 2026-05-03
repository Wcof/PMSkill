# Codex 安装说明

## Step 0：默认完整安装

推荐使用免交互安装，避免安装器英文提示干扰：

```bash
npx skills@latest add Wcof/PRDContextEngine --all
```

也可以运行 skills.sh 交互安装器（installer）：

```bash
npx skills@latest add Wcof/PRDContextEngine
```

选择 `prd-helper`，并选择 Codex 作为安装目标。这个 Skill 内部包含采集、精炼、关联、生成四个模块，不拆分安装。

交互选择时：

- 使用 `↑` / `↓` 移动
- 使用 `Space` 勾选或取消
- 使用 `Enter` 确认
- 不需要输入数字

安装完成后，在 Codex 中运行：

```text
/prd-helper
```

首次运行 `/prd-helper` 会自动初始化项目：创建 `docs/prd-helper/`，并写入 `AGENTS.md` 配置块。

## 卸载

在 Codex 对话中发送：

```text
/prd-remove
```

Agent 会清理 `AGENTS.md` 中的 PRD Helper 配置块，然后从当前项目卸载 Codex 中的 PRD Helper Skill。

如果需要手动执行同等命令：

```bash
python3 .agents/skills/prd-helper/scripts/remove-prd-helper.py --agent codex --project .
```

如果当初是全局安装：

```bash
npx skills@latest remove prd-helper --agent codex --global -y
```

交互式卸载：

```bash
npx skills@latest remove
```

卸载 Skill 不会自动删除 `docs/prd-helper/` 中已经生成的 PRD 文档。

## 手动安装步骤（备选）

1. 将本仓库复制到目标项目的 `.agents/repository root/`：

```bash
cp -r /path/to/PRDContextEngine /path/to/your-project/.agents/repository root
```

2. 将 `support/adapters/codex/AGENTS.md` 复制到目标项目根目录：

```bash
cp /path/to/PRDContextEngine/support/adapters/codex/AGENTS.md /path/to/your-project/AGENTS.md
```

3. 如果目标项目已有 `AGENTS.md`，将内容追加到现有文件中。

## 验证安装

安装完成后，目标项目结构应如下：

```
your-project/
├── AGENTS.md                          # Codex Agent 指令
├── .agents/
│   └── skills/
│       └── prd-helper/
│           ├── SKILL.md
│           ├── modules/
│           ├── checks/
│           └── scripts/
└── docs/
    └── prd-helper/                    # 生成的 PRD 文档
        ├── 01-collect/
        ├── 02-refine/
        ├── 03-relate/
        ├── 04-generate/
        └── 05-check/
```

## 使用方式

安装后，先发送 `/prd-helper` 自动初始化。开始主动采集时发送：

```text
/prd-start
```

之后向 Codex 提供产品讨论、会议纪要、原型说明等材料，Codex 会按照 prd-helper skill 进行处理。
