# GitHub 项目介绍图与仓库规范落地指南

## 1) 项目介绍图 Prompt（可直接复制）

### 1.1 通用结构

按以下顺序组装：

`媒介/风格 + 主体 + 场景/动作 + 关键细节 + 技术规格`

### 1.2 本项目推荐 Prompt（中文）

```text
现代扁平数字插画风格，主题为“PRD Helper 四环节协作引擎”，画面主体是一个正在整理需求上下文的 AI 助手与产品团队，桌面上有会议纪要、客户反馈、原型草图，背景展示四个流程节点 Collect、Refine、Relate、Generate 依次点亮，强调“可追溯、可检查、可复用”的产品文档流转。构图为横向 16:9，中心主体+右侧流程图标，蓝青与深灰配色，光线清晰，信息层次明确，适合 GitHub 项目封面，输出 1280x640，干净无水印，无多余文字噪音。
```

### 1.3 Recommended Prompt (English)

```text
Modern flat digital illustration, themed as "PRD Helper four-stage collaboration engine". Main subject: an AI assistant working with a product team to organize requirement context, with meeting notes, customer feedback, and prototype sketches on the desk. Background shows four illuminated workflow nodes: Collect, Refine, Relate, Generate, emphasizing traceable, checkable, reusable PRD flow. Wide 16:9 composition, central subject with right-side process icons, blue-cyan and dark gray palette, crisp lighting, clear visual hierarchy, suitable as GitHub project social preview, 1280x640 output, clean and watermark-free.
```

### 1.4 快速迭代指令

- 加元素：`增加右侧流程卡片并突出 Collect->Generate 箭头`
- 减元素：`移除人物，仅保留抽象流程与文档资产`
- 改风格：`改为 3D isometric 风格，保留同样信息结构`
- 改比例：`改为 3:1 横幅，适配 GitHub 仓库页眉`

### 1.5 尺寸与格式建议

- 推荐：`1280 x 640`（GitHub 社交预览友好）
- 最低：`640 x 320`
- 文件大小：尽量 `< 1 MB`

## 2) 仓库结构规范（本仓库映射）

### 2.1 标准目录建议

- `modules/`：核心业务模块（本项目相当于常见 `src/`）
- `tests/`：自动化测试
- `docs/`：文档与设计说明
- `scripts/`：维护脚本与工具
- `support/assets/`：静态资源（图、适配器资产）
- `.github/`：Issue/PR 模板、CI 工作流

### 2.2 关键治理文件

- `README.md`：项目说明与快速上手
- `LICENSE`：开源许可
- `CHANGELOG.md`：版本变更记录
- `CONTRIBUTING.md`：贡献流程
- `CODE_OF_CONDUCT.md`：社区行为准则
- `SECURITY.md`：安全披露流程
- `SUPPORT.md`：支持与反馈渠道

### 2.3 持续实践建议

- 保持 commit 信息语义化且可追踪。
- 优先通过 PR 模板描述“变更内容/验证方式/风险”。
- 每次发布同步更新 `CHANGELOG.md`。
- 新增命令或模块时，同时更新 `README.md` 与对应模板文档。
