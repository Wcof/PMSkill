# 产出示例

线框图两维度输出：

**导航流（Mermaid）**：
```mermaid
flowchart LR
    Login --> Dashboard --> MemberCenter --> Upgrade
```

**页面内布局（markdown 表格）**：
```markdown
| 区域 | 组件 | 数据来源 | 类型 |
|------|------|----------|------|
| 顶部 | 用户头像+等级 | User API | 事实 |
| 中部 | 升级按钮 | - | [假设] |
| 底部 | 续费提醒开关 | Setting API | 事实 |
```

# 延伸参考

- [Mermaid flowchart docs](https://mermaid.js.org/syntax/flowchart.html)
- [PM Compass - Wireframe Design](https://www.productcompass.pm/p/what-exactly-is-product-discovery)

# 实战提示

- **图+表互补缺一不可**：图擅长导航流，表擅长组件布局细节
- **每个组件标注数据来源**：无来源的标 [假设] 不臆造
- **组件类型列帮助前端预估工作量**：按钮/输入/列表/卡片分类
- **线框只表现交互和布局**：不表达技术实现，那是 ai-prd 的职责
