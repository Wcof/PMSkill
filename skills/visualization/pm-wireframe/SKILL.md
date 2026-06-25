---
name: pm-wireframe
description: 从 PMContext 生成界面线框图。Use when the user asks for wireframe or page layout.
---

# /pm-wireframe

从 PMContext 输出界面线框图。

## 产物

写入 `docs/pm-context/sketch/wireframe.md`。

产出格式：Mermaid flowchart 画页面间导航关系 + markdown 表格画每个页面内的组件布局。

两个维度互补——图擅长导航流，表格擅长布局细节。

```markdown
# 界面线框图
## 页面导航
​```mermaid
flowchart TD
  A[首页] --> B[登录页]
  B --> C[仪表盘]
  C --> D[设置页]
​```
## 页面布局
### 首页
| 区域 | 组件 | 交互 |
|---|---|---|
| 顶部 | Logo + 导航栏 | 点击切换页面 |
| 中间 | 搜索框 | 输入关键词搜索 |
| 底部 | 快捷入口 | 点击跳转 |
### 登录页
| 区域 | 组件 | 交互 |
|---|---|---|
| 中间 | 用户名输入框 | 输入用户名 |
| 中间 | 密码输入框 | 输入密码 |
| 底部 | 登录按钮 | 提交登录 |
```

## 关联增强

确保每个图元都对应 PMContext 中的实体/关系，无法对应的图元标 `[假设]`。
