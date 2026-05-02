# 01 Collect Directory

## 中文说明

这是 PRD Helper 的信息采集目录。

- `active/`：Agent 主动采集区，由 Agent 和脚本写入。
- `passive/`：人工材料投放区。请把会议纪要、评审记录、旧 PRD、客户反馈、Word、PDF、Markdown、TXT 等原始材料直接放到这里。
- `source-index.md`：材料索引，供下一环节精炼读取。
- `collect-state.md`：采集状态，记录当前采集 session、写入路径和时间戳。
- `collect-summary.md`：采集摘要，只做轻量说明，不做事实提取。
- `check.md`：采集检查结果。

### 被动材料元信息格式

建议每份 Markdown/TXT 被动材料都包含中英文双语字段，方便人类阅读和 Agent/脚本稳定识别：

```markdown
- 材料类型 / source_type：
- 来源 / source：
- 记录时间 / source_time：
- 记录人 / recorder：
- 责任人 / owner：
- 优先级 / priority：高 / 中 / 低；high / medium / low
```

注意：不要改写 `passive/` 中的原始材料。Agent 只扫描、索引和标记元信息。

## English

This is the PRD Helper collect directory.

- `active/`: Agent-managed active capture area.
- `passive/`: User-managed passive source drop zone. Put meeting notes, review records, legacy PRDs, customer feedback, Word, PDF, Markdown, TXT, and other raw materials here.
- `source-index.md`: Source index for the next refine step.
- `collect-state.md`: Capture state, including session, write roots, and timestamps.
- `collect-summary.md`: Lightweight collection summary, not fact extraction.
- `check.md`: Collect check result.

### Passive Source Metadata

Each Markdown/TXT passive source should include bilingual metadata fields so both humans and agents can read them consistently:

```markdown
- 材料类型 / source_type:
- 来源 / source:
- 记录时间 / source_time:
- 记录人 / recorder:
- 责任人 / owner:
- 优先级 / priority: high / medium / low
```

Do not rewrite raw files in `passive/`. The Agent should only scan, index, and mark metadata.
