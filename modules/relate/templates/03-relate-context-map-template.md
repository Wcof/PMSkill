# 上下文总关联图

## 0. 关联图信息

- 来源范围：
- 当前状态：已确认 / 待确认
- 待确认项：

## 1. 需求到页面

- fact_001 → page_001

## 2. 页面到功能

- page_001 → feature_001

## 3. 功能到规则

- feature_001 → rule_001

## 4. 规则到数据

- rule_001 → data_001

## 5. 规则到验收

- rule_001 → acceptance_001

## 6. 待确认问题影响范围

- question_001 → page_001 / rule_001 / data_001

## 7. 冲突点影响范围

- conflict_001 → page_001 / rule_001

## 8. AI 推断影响范围

- assumption_001 → rule_001 / data_001
