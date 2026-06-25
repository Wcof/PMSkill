---
name: pm-state
description: 从 PMContext 生成状态机图。Use when the user asks for state machine or state transitions.
---

# /pm-state

从 PMContext 输出状态机图。

## 产物

写入 `docs/pm-context/sketch/state.md`。

产出格式：Mermaid stateDiagram-v2，状态节点 + 转移边 + 条件标注。

```markdown
# 状态机图
​```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Submitted: 提交
  Submitted --> InReview: 开始评审
  InReview --> Approved: 通过
  InReview --> Rejected: 驳回
  Rejected --> Draft: 修改后重新提交
  Approved --> [*]
​```
```

## 关联增强

确保每个图元都对应 PMContext 中的实体/关系，无法对应的图元标 `[假设]`。
