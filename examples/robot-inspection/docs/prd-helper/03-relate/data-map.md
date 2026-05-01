# 数据关联图

## data_001：地图（Map）

- 对象含义：巡检区域的地理容器
- 来源事实：fact_003
- 关联页面：page_001、page_002
- 关联功能：feature_001
- 关联规则：rule_001
- 关键字段：id、name、description、create_time
- 状态字段：status（已创建、已发布）
- 待确认问题：

## data_002：区域（Zone）

- 对象含义：地图上的巡检区域
- 来源事实：fact_003
- 关联页面：page_002
- 关联功能：feature_002
- 关联规则：rule_002
- 关键字段：id、name、map_id、boundary、area_type
- 状态字段：status（已划分、已发布）
- 待确认问题：question_003

## data_003：巡检点（InspectionPoint）

- 对象含义：业务人员理解的巡检单元
- 来源事实：fact_001
- 关联页面：page_003
- 关联功能：feature_003
- 关联规则：rule_003
- 关键字段：id、name、code、zone_id、robot_points
- 状态字段：status（已创建、已启用、已停用）
- 待确认问题：question_001

## data_004：机器人点位（RobotPoint）

- 对象含义：机器人执行的细粒度点位
- 来源事实：fact_001、fact_002
- 关联页面：page_004
- 关联功能：feature_004
- 关联规则：rule_004
- 关键字段：id、name、code、inspection_point_id、coordinates、collection_points
- 状态字段：status（已创建、已启用、已停用）
- 待确认问题：

## data_005：设施设备（Facility）

- 对象含义：被巡检的设施设备
- 来源事实：fact_004
- 关联页面：page_005、page_006
- 关联功能：feature_005
- 关联规则：rule_005
- 关键字段：id、name、code、type、location、components
- 状态字段：status（已录入、已启用、已停用）
- 待确认问题：question_002

## data_006：设施部件（Component）

- 对象含义：设施设备的组成部分，如阀门、仪表
- 来源事实：fact_004、fact_006
- 关联页面：page_006
- 关联功能：feature_006
- 关联规则：rule_006
- 关键字段：id、name、code、facility_id、type、inspection_lines
- 状态字段：status（已关联、已启用、已停用）
- 待确认问题：question_004

## data_007：任务（Task）

- 对象含义：一次具体的巡检执行任务
- 来源事实：fact_005、fact_007
- 关联页面：page_007
- 关联功能：feature_007
- 关联规则：rule_007
- 关键字段：id、name、plan_id、robot_id、execute_time、inspection_points、status
- 状态字段：status（待执行、执行中、已完成、已中断、已取消）
- 待确认问题：

## data_008：巡检计划（Plan）

- 对象含义：巡检任务的执行计划
- 来源事实：fact_005
- 关联页面：page_008
- 关联功能：feature_008
- 关联规则：rule_008
- 关键字段：id、name、execute_cycle、inspection_points、inspection_lines
- 状态字段：status（已创建、已启用、已停用）
- 待确认问题：

## data_009：检测线（InspectionLine）

- 对象含义：一组检测动作的集合
- 来源事实：fact_006
- 关联页面：page_006
- 关联功能：feature_006
- 关联规则：rule_006
- 关键字段：id、name、component_id、detection_actions
- 状态字段：status（已创建、已启用、已停用）
- 待确认问题：question_004
