# 产出示例

`/pm-sketch --auto 会员中心` 产出：

```
docs/pm-context/sketch/
├── wireframe.md    # 页面导航图 + 3 页布局表格
├── ia.md           # 实体关系图（会员/订单/积分）
├── state.md        # 会员状态机（待激活/活跃/已过期/已冻结）
├── flow.md         # 续费流程图（含异常路径）
└── prototype.html  # 高保真交互原型（单页 HTML，无外部依赖）
```

# 延伸参考

- [Mermaid stateDiagram-v2 docs](https://mermaid.js.org/syntax/stateDiagram.html)
- [Mermaid flowchart docs](https://mermaid.js.org/syntax/flowchart.html)
- [HTML 原型设计原则](https://www.productcompass.pm/p/the-extended-opportunity-solution-tree)

# 实战提示

- **`--prototype` 优先于 Mermaid 盲出**：HTML 交互原型比 4 张静态图更能暴露 UX 问题
- **质量清单过一遍**：HTML 生成后逐项检查 9 点（断网可预览、[假设] 标注、响应式等）
- **Mermaid 渲染卡顿**：节点 > 30 时拆成子图或分文件，不要硬塞一个图里
