# Claude Code 安装说明

## 安装步骤

1. 将 `skills/prd-context/` 目录复制到目标项目的 `.claude/skills/prd-context/`：

```bash
cp -r skills/prd-context/ /path/to/your-project/.claude/skills/prd-context/
```

2. 将 `adapters/claude-code/CLAUDE.md` 复制到目标项目根目录：

```bash
cp adapters/claude-code/CLAUDE.md /path/to/your-project/CLAUDE.md
```

3. 如果目标项目已有 `CLAUDE.md`，将内容追加到现有文件中。

## 验证安装

安装完成后，目标项目结构应如下：

```
your-project/
├── CLAUDE.md                          # Claude Code 指令
├── .claude/
│   └── skills/
│       └── prd-context/
│           ├── SKILL.md
│           ├── references/
│           ├── assets/
│           │   └── templates/
│           └── scripts/
└── docs/
    └── prd-context/                   # 生成的 PRD 上下文
```

## 使用方式

安装后，当向 Claude Code 提供产品讨论、会议纪要、原型说明等材料时，Claude Code 会自动使用 prd-context skill 进行处理。
