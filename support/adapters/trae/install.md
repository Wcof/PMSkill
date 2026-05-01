# Trae 安装说明

## 安装步骤

1. 将本仓库复制到目标项目中（路径按 Trae 当前版本调整）：

```bash
cp -r /path/to/PRDContextEngine /path/to/your-project/repository root
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

安装后，当向 Trae Agent 提供产品讨论、会议纪要、原型说明等材料时，Trae 会按照 project_rules.md 中定义的流程进行处理。

## 注意

Trae 的实际 Skill 文件落点需要在实现时根据当前版本验证。上述安装路径为建议路径。
