# 采集检查

## 0. 检查信息

- 检查来源：
- 检查状态：通过 / 不通过 / 待确认
- 待确认项：

## 1. 状态与目录检查

- [ ] 通过 `/prd-start` 开启过采集 session
- [ ] `collect-state.md` 存在且可读
- [ ] `active/` 目录存在
- [ ] `passive/` 目录存在
- [ ] `source-index.md` 存在

## 2. 主动采集检查

- [ ] `capture_mode` 状态正确
- [ ] `active/sessions/` 存在
- [ ] 主动采集记录完整保存 User Query
- [ ] 主动采集记录完整保存 Agent Answer
- [ ] 主动采集记录包含 YAML front matter

## 3. 被动采集检查

- [ ] `passive/` 可以被扫描
- [ ] 被动材料已进入 `source-index.md`
- [ ] 未改写 `passive/` 中的原始文件
- [ ] 元信息缺失时标记为 `metadata_status: missing`

## 4. 索引与原文保留检查

- [ ] `source-index.md` 引用的文件路径真实存在
- [ ] 未提前改写成 PRD
- [ ] 未混入 AI 推断
- [ ] 噪音只标记 `noise_hint`，不删除原文

## 5. 采集结论

本轮采集是否可以进入精炼阶段：

- [ ] 可以
- [ ] 不可以
- 原因：
