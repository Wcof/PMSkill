---
name: pm-flow
description: 从 PMContext 生成流程图。Use when the user asks for flowchart or process flow.
---

# /pm-flow

从 PMContext 输出流程图。

## 产物

写入 `docs/pm-context/sketch/flow.md`。

产出格式：Mermaid flowchart，步骤节点 + 判断分支 + 异常路径。

```markdown
# 流程图
​```mermaid
flowchart TD
  A[用户发起请求] --> B{是否已登录?}
  B -->|是| C[处理请求]
  B -->|否| D[跳转登录页]
  D --> E[登录成功]
  E --> C
  C --> F{请求是否合法?}
  F -->|是| G[返回结果]
  F -->|否| H[返回错误]
​```
```

## 关联增强

确保每个图元都对应 PMContext 中的实体/关系，无法对应的图元标 `[假设]`。
