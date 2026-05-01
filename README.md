# PRD Helper

## 第一部分：怎么用（给小白）

1. 把本仓库放到你使用的 Agent Skill 目录里。
2. 把产品材料交给 Agent（会议纪要、聊天记录、原型说明、客户反馈、历史文档）。
3. Agent 会按四步处理：Collect → Refine → Relate → Generate。
4. 产物输出到目标项目 `docs/prd-helper/`。
5. 运行检查脚本确认结果质量：

```bash
python3 scripts/check-structure.py examples/robot-inspection/docs/prd-helper
python3 scripts/check-relations.py examples/robot-inspection/docs/prd-helper
python3 scripts/check-generated.py examples/robot-inspection/docs/prd-helper
```

## 第二部分：项目介绍

### 2.1 简单介绍

PRD Helper 是一个把“原始沟通材料”转成“结构化 PRD 上下文”的 Skill 项目。
它的目标是让产品、前后端、测试和 Agent 都能拿到可追溯、可复用、可检查的统一上下文。

### 2.2 专业介绍（结构 + 模块职责）

当前项目结构如下：

```text
PRDContextEngine/
├── README.md
├── SKILL.md
├── modules/
│   ├── collect/
│   ├── refine/
│   ├── relate/
│   └── generate/
├── checks/
├── scripts/
├── examples/
└── support/
```

各部分职责：

- `SKILL.md`：Skill 主入口，定义流程和执行约束。
- `modules/collect/`：采集模块，保存原始材料，不提前下结论。
- `modules/refine/`：精炼模块，提取事实、目标、约束、冲突、问题与推断。
- `modules/relate/`：关联模块，建立需求到页面/功能/规则/数据/验收的链路。
- `modules/generate/`：生成模块，输出页面、规则、数据、验收、Agent 上下文文档。
- `checks/`：横向质量门禁（不是第五业务模块），负责阶段检查与最终检查模板。
- `scripts/`：自动检查脚本（结构、关系、生成质量）。
- `examples/`：可直接参考的示例项目。
- `support/`：适配器文档、历史资料和辅助资产。

## 一张图教会你 PRD Helper 项目

![一张图教会你 PRD Helper 项目](support/assets/prd-helper-project-overview.svg)
