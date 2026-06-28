# 产出示例

假设 `$ARGUMENTS = "会员中心"`，扫描结果：

```
集合: docs/pm-context/collect/collect.md

## 项目深扫描
### 来源索引
- 来源：项目深扫描
- 路径：./README.md
### 概要
README 提到"会员中心将在 v2.0 上线"，无具体细节
### 关键信息
- 会员中心在 TODO list 中（← README）
- 代码中已存在 `app/controllers/member*` 目录（← 目录扫描）
- git log 显示"add: 会员表 migration"（← git history）

## 用户反馈（对话上下文）
### 来源索引
- 来源：对话
- 时间：2024-06-28
### 关键信息
- 用户说："会员续费太麻烦了，每次要重新填信息"
```

# 延伸参考

- [PM Compass - Product Discovery Guide](https://www.productcompass.pm/p/what-exactly-is-product-discovery)
- [Opportunity Solution Tree](https://www.productcompass.pm/p/the-extended-opportunity-solution-tree)

# 实战提示

- **4 源扫描按优先级走**：对话上下文 → 项目深扫描 → URL → 知识库。前两个通常够用
- **URL 抓取失败常见**：设 10s 超时，失败的不阻塞流程，标记到信息缺口即可
- **git log 扫描只取最近 30 条**：太多 commit 会产生噪音
