# 4 源扫描产出示例与配置技巧

## 完整产出

假设 `$ARGUMENTS = "会员中心"`，4 源扫描结果：

### URL 抓取
```markdown
## 竞品分析报告
### 来源索引
- 来源：URL
- 路径：https://competitor.example.com/pricing
- 时间：2026-06-29
### 概要
竞品 A 年付价格 = 月付 × 9，转化率 22%；竞品 B 年付 = 月付 × 10，转化率 18%
### 关键信息
- 年付倍数 9-10 是行业惯例
- 转化率 > 15% 即视为成功
### 与其他材料的关联
- 与对话中"用户想要年付"互相印证
```

### 对话上下文
```markdown
## 用户反馈
### 来源索引
- 来源：对话
- 时间：2026-06-29
### 关键信息
- 用户说："会员续费太麻烦了，每次要重新填信息"
- 用户说："想要年付但没选项"
### 与其他材料的关联
- 与 URL 竞品分析中的"年付转化率 22%"互相印证
```

### 项目深扫描
```markdown
## 项目深扫描
### 来源索引
- 来源：项目深扫描
- 路径：./README.md, ./docs/, ./src/
### 概要
项目使用 Node.js + PostgreSQL，已有 payment 模块，会员模块待建
### 关键信息
- README 提到"会员中心将在 v2.0 上线"
- 代码中已存在 `src/modules/payment/` 目录
- git log 显示"add: 会员表 migration"
- TODO: 5 处（3 处有产品含义：添加年付选项、续费提醒、会员等级）
### 与其他材料的关联
- git log "会员表 migration" 与对话中"续费太麻烦"指向同一需求
```

### 知识库搜索
```markdown
## 用户调研报告
### 来源索引
- 来源：知识库
- 路径：~/docs/pm-kb/user-research-2026-Q2.md
### 关键信息
- NPS 评分：续费体验 32 分（低于基准 50 分）
- 80% 受访者希望"提前一周收到续费提醒"
### 与其他材料的关联
- 与对话中"续费太麻烦"互相印证
```

## 4 源扫描配置技巧

| 技巧 | 说明 |
|------|------|
| **按优先级走** | 对话上下文 → 项目深扫描 → URL → 知识库，前两个通常够用 |
| **URL 抓取设超时** | 10s 超时，失败的不阻塞流程，标记到信息缺口 |
| **git log 只取最近 30 条** | 太多 commit 产生噪音 |
| **TODO/FIXME 过滤产品含义** | "TODO: 重构函数"不收集，"TODO: 添加支付"才收集 |
| **知识库按需搜索** | 不全量读，按当前需求主题筛选相关段落 |
| **去重是 collect 职责** | 同一信息出现在 URL 和对话中，保留首条，后续标 `← 重复` |

## 延伸参考

- [PM Compass - Product Discovery Guide](https://www.productcompass.pm/p/what-exactly-is-product-discovery)
- [Opportunity Solution Tree](https://www.productcompass.pm/p/the-extended-opportunity-solution-tree)
