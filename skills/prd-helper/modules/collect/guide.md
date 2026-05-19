# Collect 模块指南

## 职责

通过主动采集和被动采集两种方式，把原始产品上下文持续、可追溯地写入材料库，并生成索引和轻量摘要，为下一环节"精炼"做准备。

采集模块只负责：收集材料、保存原文、记录元信息、建立索引、生成轻量摘要、标记噪音、处理增量写入、记录异常情况。

采集模块不负责：不做事实提取、不做深度清洗、不做业务推理、不做冲突消解、不做最终结论、不生成 PRD、不把 AI 推断写成确定事实。

> 采集模块负责"把材料收好、标好、排好队"，不负责"把材料想明白"。

## 核心约束

1. **只有用户显式触发 `/prd-start` 后才进入主动采集。**
2. 主动采集最小单位是完整 `User Query + Agent Answer`。
3. `/prd-stop` 后必须关闭主动采集、清理 hooks、生成摘要和检查。
4. stop 后再次 `/prd-start` 应复用当前 session，避免把同一次产品讨论拆散。
5. **每次主动采集必须调用脚本写入，不能只在回复里声称已记录。**
6. `/prd-scan` 可以独立导入历史 Agent 会话，不要求先执行 `/prd-start`。
7. `/prd-import` 和被动材料扫描只能索引原始文件，不能改写原文件。
8. 不做事实提取、不清洗、不生成 PRD。
9. 不把 AI 推断写成确定事实。

## 主动采集

### 采集命令

| 命令 | 含义 | 结果 |
|------|------|------|
| `/prd-start` | 开启 PRD Capture Session | 设置 `capture_mode: on`，创建 session |
| `/prd-stop` | 关闭 PRD Capture Session | 设置 `capture_mode: off`，生成摘要和检查 |
| `/prd-status` | 查看采集状态 | 返回当前 session、turn 数、最近采集时间等 |
| `/prd-scan` | 扫描所有 AI 工具 session | 扫描 Claude Code、Cursor、Trae、Codex 的项目 session 并批量采集 |
| `/prd-import` | 导入第三方文件夹数据 | 复制或登记为被动材料，并更新 source-index |

### 执行保证

Agent 不能只回复"已开启采集"，必须真实写入状态文件和 session 文件。

- **状态文件证明已开启**：`collect-state.md`
- **统一脚本保证写入路径和格式**：`capture-source.py`
- **检查脚本验证是否真的采集成功**：`check-collect.py`

### 每轮采集记录

当 `capture_mode == on` 时，Agent 在每轮对话结束后自动写入：

```bash
python3 modules/collect/scripts/capture-source.py \
  --agent codex \
  --user-query-file /tmp/user-query.txt \
  --agent-answer-file /tmp/agent-answer.txt
```

记录内容包括：User Query 原文、Agent Answer 原文、元信息、content_hash、轻量噪音提示。

## 批量扫描采集

`/prd-scan` 扫描当前项目在所有 AI 编码工具中的历史 session，一次性批量采集。

### 支持的工具

| 工具 | 存储位置 | 说明 |
|------|---------|------|
| Claude Code | `~/.claude/projects/` | JSONL session 文件 |
| Cursor | `~/Library/Application Support/Cursor/` | SQLite composerData |
| Trae / Trae CN | `~/Library/Application Support/Trae[ CN]/` | SQLite agent storage |
| Codex | `~/.codex/sessions/` | JSONL session 文件 |

### 去重策略

1. **文件名快速跳过** — 已存在的 `session-{tool}-{id}.md` 直接跳过
2. **content_hash 精确去重** — 新 session 计算 sha256 哈希，与 source-index.md 比对

### 使用方式

```bash
python3 modules/collect/scripts/collect-control.py scan --project /path/to/project
```

或通过 Agent 指令：`/prd-scan`

`/prd-scan` 可独立运行，无需先执行 `/prd-start`。如果 collect-state.md 不存在，会自动创建目录结构和状态文件。

## 被动采集

用户直接把已有材料放入：

```text
docs/prd-helper/01-collect/passive/
```

Agent 对被动材料只做：扫描文件、识别路径、计算 content_hash、建立 source-index、标记元信息缺失。

**Agent 不改写 `passive/` 里的原始文件。**

建议 Markdown/TXT 被动材料使用中英文双语元信息字段，便于人类阅读和 Agent/脚本识别：

```markdown
- 材料类型 / source_type：
- 来源 / source：
- 记录时间 / source_time：
- 记录人 / recorder：
- 责任人 / owner：
- 优先级 / priority：高 / 中 / 低；high / medium / low
```

脚本会同时识别中文字段、英文字段和 YAML front matter；缺失时只标记 `metadata_status: missing`，不伪造信息。

## 外部导入

`/prd-import` 用于把第三方文件夹中的旧 PRD、会议纪要、客户反馈、原型说明等材料纳入 `01-collect/passive/`。

导入边界：

- 只导入和索引原始材料，不把内容提前拆成事实或规则。
- 保留文件来源、路径、hash、导入时间和元信息状态。
- 同名或同内容文件必须通过 hash 去重，不能重复污染 `source-index.md`。
- 导入后仍由 Refine 阶段决定哪些内容成为事实、问题、冲突或推断。

## 输出结构

```text
docs/prd-helper/01-collect/
├── README.md
├── active/
│   ├── sessions/
│   ├── historical/
│   └── anomalies/
├── passive/
├── source-index.md
├── collect-summary.md
├── collect-state.md
└── check.md
```

### 各文件职责

| 文件 | 职责 |
|------|------|
| `collect-state.md` | 采集状态唯一事实源（capture_mode、session_id、写入路径、时间戳） |
| `source-index.md` | 材料索引事实源，给下一环节读取 |
| `collect-summary.md` | 轻量采集摘要，不做事实提取 |
| `check.md` | 采集检查结果 |
| `active/sessions/` | 主动采集的 conversation turn |
| `active/historical/` | 补录的历史材料 |
| `active/anomalies/` | 异常材料 |
| `passive/` | 用户投放的被动材料 |

## 噪音提示

采集阶段允许噪音存在，但不做最终处理。

- `noise_hint: none` — 暂未发现明显噪音特征
- `noise_hint: possible_noise` — 可能是噪音，留给精炼环节判断

精炼阶段才负责最终处理噪音。

## 增量写入

每次写入前，比较新材料的 `source_time` 和 `collect-state.md` 中的 `last_collect_at`：

- `source_time > last_collect_at` → 正常写入
- `source_time == last_collect_at` → 比较 content_hash 判断是否重复
- `source_time < last_collect_at` → 异常/历史补录，写入 anomalies 或 historical

## 验收条件

| 验收项 | 期望结果 |
|--------|----------|
| `/prd-start` | 创建 `collect-state.md`、`active/`、`passive/`、`source-index.md` |
| `/prd-status` | 能读取真实状态，不靠口头记忆 |
| 主动写入 | `capture_mode == on` 时写入完整 User Query + Agent Answer |
| `/prd-stop` | 关闭采集，生成 `collect-summary.md` 和 `check.md` |
| `/prd-scan` | 可独立扫描历史 Agent session 并批量采集 |
| `/prd-import` | 可导入外部文件夹作为被动材料 |
| 被动扫描 | `scan-passive.py` 能扫描 `passive/` 并更新索引 |
| 原文保留 | 主动和被动材料都不被提前清洗 |
| 索引可用 | `source-index.md` 引用的文件路径真实存在 |
| 检查通过 | `check-collect.py` 能输出采集模块是否可进入精炼 |

## 下一步

通过检查后进入 **Refine（精炼）** 阶段。
