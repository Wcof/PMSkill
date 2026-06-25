---
name: pm-ia
description: 从 PMContext 生成信息架构图。Use when the user asks for information architecture or entity relationships.
---

# /pm-ia

从 PMContext 输出信息架构图。

## 产物

写入 `docs/pm-context/sketch/ia.md`。

产出格式：Mermaid graph/flowchart，节点为实体/页面，边为导航/包含关系。

```markdown
# 信息架构图
​```mermaid
graph TD
  App[应用] --> Auth[认证模块]
  App --> Core[核心业务]
  Auth --> User[用户]
  Auth --> Session[会话]
  Core --> Order[订单]
  Core --> Product[商品]
  Order --> OrderItem[订单项]
​```
```

## 关联增强

确保每个图元都对应 PMContext 中的实体/关系，无法对应的图元标 `[假设]`。
