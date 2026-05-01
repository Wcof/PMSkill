# 数据说明：巡检域数据模型

## 1. 数据域说明

巡检域包含地图、区域、巡检点、机器人点位、设施设备、设施部件、任务、巡检计划、检测线等核心业务对象。

## 2. 核心业务对象

| 对象 | 含义 | 来源 |
|---|---|---|
| Map | 地图，巡检区域的地理容器 | fact_003 |
| Zone | 区域，地图上的巡检区域 | fact_003 |
| InspectionPoint | 巡检点，业务人员理解的巡检单元 | fact_001 |
| RobotPoint | 机器人点位，机器人执行的细粒度点位 | fact_001、fact_002 |
| Facility | 设施设备，被巡检的设施设备 | fact_004 |
| Component | 设施部件，设施设备的组成部分 | fact_004、fact_006 |
| Task | 任务，一次具体的巡检执行任务 | fact_005、fact_007 |
| Plan | 巡检计划，巡检任务的执行计划 | fact_005 |
| InspectionLine | 检测线，一组检测动作的集合 | fact_006 |

## 3. 对象关系

| 对象 A | 关系 | 对象 B |
|---|---|---|
| Map | 1:N | Zone |
| Zone | 1:N | InspectionPoint |
| InspectionPoint | 1:N | RobotPoint |
| RobotPoint | 1:N | CollectionPoint |
| Facility | 1:N | Component |
| Component | 1:N | InspectionLine |
| Plan | 1:N | Task |
| Task | N:N | InspectionPoint |
| Task | N:1 | Robot |

## 4. 关键字段

| 对象 | 字段 | 含义 | 状态 |
|---|---|---|---|
| Map | id | 地图ID | 已确认 |
| Map | name | 地图名称 | 已确认 |
| Zone | id | 区域ID | 已确认 |
| Zone | map_id | 所属地图 | 已确认 |
| InspectionPoint | id | 巡检点ID | 已确认 |
| InspectionPoint | zone_id | 所属区域 | 已确认 |
| RobotPoint | id | 机器人点位ID | 已确认 |
| RobotPoint | inspection_point_id | 所属巡检点 | 已确认 |
| Facility | id | 设施设备ID | 已确认 |
| Facility | code | 设施设备编号 | 已确认 |
| Component | id | 部件ID | 已确认 |
| Component | facility_id | 所属设施设备 | 已确认 |
| Task | id | 任务ID | 已确认 |
| Task | plan_id | 来源计划 | 已确认 |
| Plan | id | 计划ID | 已确认 |

## 5. 状态字段

| 对象 | 状态 | 含义 |
|---|---|---|
| Map | 已创建、已发布 | 地图生命周期 |
| InspectionPoint | 已创建、已启用、已停用 | 巡检点生命周期 |
| RobotPoint | 已创建、已启用、已停用 | 机器人点位生命周期 |
| Facility | 已录入、已启用、已停用 | 设施设备生命周期 |
| Task | 待执行、执行中、已完成、已中断、已取消 | 任务生命周期 |
| Plan | 已创建、已启用、已停用 | 计划生命周期 |

## 6. 生命周期

- 地图：创建 → 发布 → 使用
- 巡检点：创建 → 启用 → 停用
- 设施设备：录入 → 启用 → 停用
- 任务：待执行 → 执行中 → 已完成/已中断/已取消
- 计划：创建 → 启用 → 停用

## 7. 数据来源

- 地图、区域：用户手动创建
- 巡检点、机器人点位：用户手动创建
- 设施设备：用户手动录入或批量导入
- 任务：从计划自动派生或手动创建
- 计划：用户手动创建

## 8. 数据去向

- 检测结果记录到设施设备或部件
- 任务执行记录关联到巡检点和机器人点位

## 9. 与现有表结构关系

待确认：需要了解现有数据库表结构。

## 10. 待确认问题

- question_002：批量导入的技术方案
- question_004：检测线的具体定义

## 11. 来源说明

本数据说明基于：产品口述、会议纪要、原型说明。
