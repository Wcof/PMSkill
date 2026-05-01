# 上下文总关联图

## 1. 需求到页面

- fact_001 → page_003、page_004
- fact_002 → page_004
- fact_003 → page_001、page_002
- fact_004 → page_005、page_006
- fact_005 → page_007、page_008
- fact_006 → page_006
- fact_007 → page_007
- fact_008 → page_005
- fact_009 → page_003
- fact_010 → page_003
- fact_011 → page_004
- fact_012 → page_005

## 2. 页面到功能

- page_001 → feature_001
- page_002 → feature_001、feature_002
- page_003 → feature_003
- page_004 → feature_004
- page_005 → feature_005
- page_006 → feature_006
- page_007 → feature_007
- page_008 → feature_008

## 3. 功能到规则

- feature_001 → rule_001
- feature_002 → rule_002
- feature_003 → rule_003
- feature_004 → rule_004
- feature_005 → rule_005
- feature_006 → rule_006
- feature_007 → rule_007
- feature_008 → rule_008

## 4. 规则到数据

- rule_001 → data_001
- rule_002 → data_002
- rule_003 → data_003
- rule_004 → data_004
- rule_005 → data_005
- rule_006 → data_006、data_009
- rule_007 → data_007
- rule_008 → data_008

## 5. 规则到验收

- rule_001 → acceptance_001
- rule_002 → acceptance_001
- rule_003 → acceptance_002
- rule_004 → acceptance_003
- rule_005 → acceptance_004
- rule_006 → acceptance_004
- rule_007 → acceptance_005
- rule_008 → acceptance_006

## 6. 待确认问题影响范围

- question_001 → page_003、rule_003、data_003
- question_002 → page_005、rule_005、data_005
- question_003 → page_002、rule_002、data_002
- question_004 → page_006、rule_006、data_006、data_009

## 7. 冲突点影响范围

- conflict_001 → page_005、rule_005、data_005

## 8. AI 推断影响范围

- assumption_001 → page_004、rule_004、data_004
- assumption_002 → page_002、rule_002、data_002
- assumption_003 → page_006、rule_006、data_009
- assumption_004 → page_002、page_007、rule_007、data_007
- assumption_005 → page_005、rule_005、data_005、acceptance_004
- assumption_006 → data_003、data_004、data_005、data_006、data_007
- assumption_007 → page_002、page_007、rule_007、data_007、agent-context/frontend-context.md
