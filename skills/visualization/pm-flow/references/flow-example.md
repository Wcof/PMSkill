# 产出示例

Mermaid 流程图片段：

```mermaid
flowchart TD
    A[用户发起升级] --> B{当前等级?}
    B -->|基础| C[计算差价按比例]
    B -->|高级| D[拒绝: 已是最高]
    C --> E{支付成功?}
    E -->|是| F[立即生效+发通知]
    E -->|否| G[回滚+提示重试]
    G --> A
```

# 延伸参考

- [Mermaid flowchart docs](https://mermaid.js.org/syntax/flowchart.html)
- [PM Compass - Process Design](https://www.productcompass.pm/p/what-exactly-is-product-discovery)

# 实战提示

- **判断节点必须双向**：yes/no 都要画，只画正向路径是设计缺陷
- **循环必须配退出条件**：`G -->|重试3次后| H[转人工]`
- **步骤描述含「等」即不可执行**：「等待用户确认」要改为具体触发条件
- **异常路径比正向更重要**：支付失败、超时、取消都要有兜底分支
