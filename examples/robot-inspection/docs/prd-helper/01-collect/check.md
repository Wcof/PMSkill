# 采集检查

## 0. 检查信息

- 检查来源：check-collect.py 自动生成
- 检查状态：通过
- 待确认项：无

## 1. 状态与目录检查

- [x] 通过 `/prd-start` 开启过采集 session
- [x] `collect-state.md` 存在且可读
- [x] `active/` 目录存在
- [x] `passive/` 目录存在
- [x] `source-index.md` 存在

## 2. 主动采集检查

- [x] `capture_mode` 状态正确
- [x] `active/sessions/` 存在
- [x] 主动采集记录完整保存 User Query
- [x] 主动采集记录完整保存 Agent Answer
- [x] 主动采集记录包含 YAML front matter

## 3. 被动采集检查

- [x] `passive/` 可以被扫描
- [x] 被动材料已进入 `source-index.md`
- [x] 未改写 `passive/` 中的原始文件
- [x] 元信息缺失时标记为 `metadata_status: missing`

## 4. 索引与原文保留检查

- [x] `source-index.md` 引用的文件路径真实存在
- [x] 未提前改写成 PRD
- [x] 未混入 AI 推断
- [x] 噪音只标记 `noise_hint`，不删除原文

## 5. 采集结论

本轮采集是否可以进入精炼阶段：

- [x] 可以
- [ ] 不可以
- 原因：自动检查全部通过（5 条来源，1 个 session 文件）
