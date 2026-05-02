"""
ID 注册表 — 所有实体类型的唯一真实来源。

脚本和模板都应引用此注册表来获取：
- ID 前缀（如 "fact"、"rule"）
- ID 正则模式（如 r"fact[_-]\d+"）
- 来源模块（refine / relate）
- 每个实体类型的必填字段
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class EntityType:
    prefix: str
    label: str
    source_module: str
    required_fields: tuple[str, ...] = ()
    id_pattern: str = ""
    filename: str = ""  # 对应的 Markdown 文件名（如 "facts.md"）

    def __post_init__(self):
        if not self.id_pattern:
            object.__setattr__(self, "id_pattern", rf"{self.prefix}[_-]\d+")

    def extract_ids(self, content: str) -> set[str]:
        """从 Markdown 内容中提取该类型的所有 ID。"""
        return set(re.findall(self.id_pattern, content))


# ── 精炼模块（refine）实体 ──────────────────────────────

FACT = EntityType(
    prefix="fact",
    label="需求事实",
    source_module="refine",
    required_fields=("来源材料", "来源位置", "状态"),
    filename="facts.md",
)

DECISION = EntityType(
    prefix="decision",
    label="设计决策",
    source_module="refine",
    required_fields=("来源材料", "来源位置", "状态"),
    filename="decisions.md",
)

CONSTRAINT = EntityType(
    prefix="constraint",
    label="业务约束",
    source_module="refine",
    required_fields=("来源材料", "来源位置", "状态"),
    filename="constraints.md",
)

GOAL = EntityType(
    prefix="goal",
    label="业务目标",
    source_module="refine",
    required_fields=("来源材料", "状态"),
    filename="goals.md",
)

CONFLICT = EntityType(
    prefix="conflict",
    label="冲突点",
    source_module="refine",
    required_fields=("涉及来源", "当前状态"),
    filename="conflicts.md",
)

QUESTION = EntityType(
    prefix="question",
    label="待确认问题",
    source_module="refine",
    required_fields=("来源材料", "状态"),
    filename="questions.md",
)

ASSUMPTION = EntityType(
    prefix="assumption",
    label="AI 推断",
    source_module="refine",
    required_fields=("来源材料",),
    filename="assumptions.md",
)

# ── 关联模块（relate）实体 ──────────────────────────────

PAGE = EntityType(
    prefix="page",
    label="页面",
    source_module="relate",
    required_fields=("页面路径", "所属模块", "来源范围"),
    filename="page-map.md",
)

FEATURE = EntityType(
    prefix="feature",
    label="功能",
    source_module="relate",
    required_fields=("功能说明", "来源事实"),
    filename="feature-map.md",
)

RULE = EntityType(
    prefix="rule",
    label="规则",
    source_module="relate",
    required_fields=("规则说明", "来源事实"),
    filename="rule-map.md",
)

DATA = EntityType(
    prefix="data",
    label="数据对象",
    source_module="relate",
    required_fields=("对象含义", "来源事实"),
    filename="data-map.md",
)

ACCEPTANCE = EntityType(
    prefix="acceptance",
    label="验收项",
    source_module="relate",
    required_fields=("验收目标", "来源事实"),
    filename="acceptance-map.md",
)

# ── 注册表 ──────────────────────────────────────────────

ALL_ENTITIES: tuple[EntityType, ...] = (
    FACT, DECISION, CONSTRAINT, GOAL, CONFLICT, QUESTION, ASSUMPTION,
    PAGE, FEATURE, RULE, DATA, ACCEPTANCE,
)

# 按前缀快速查找
ENTITY_BY_PREFIX: dict[str, EntityType] = {e.prefix: e for e in ALL_ENTITIES}

# 精炼模块实体列表
REFINE_ENTITIES: tuple[EntityType, ...] = tuple(
    e for e in ALL_ENTITIES if e.source_module == "refine"
)

# 关联模块实体列表
RELATE_ENTITIES: tuple[EntityType, ...] = tuple(
    e for e in ALL_ENTITIES if e.source_module == "relate"
)


# 关联链路规则。脚本使用 code，文档和检查输出使用 label。
RELATION_CHAIN_RULES: tuple[tuple[str, str, str], ...] = (
    ("fact_to_page_or_feature", "每个核心事实有关联页面或功能", "fact -> page/feature"),
    ("feature_to_rule", "每个核心功能有关联规则", "feature -> rule"),
    ("rule_to_data", "每个核心规则有关联数据对象", "rule -> data"),
    ("rule_to_acceptance", "每个核心规则有关联验收标准", "rule -> acceptance"),
    ("page_to_feature_or_rule", "每个核心页面有关联功能或规则", "page -> feature/rule"),
)


def extract_all_ids(content: str) -> dict[str, set[str]]:
    """从内容中提取所有已注册实体类型的 ID。"""
    return {e.prefix: e.extract_ids(content) for e in ALL_ENTITIES}


def entity_pattern() -> str:
    """返回匹配所有实体 ID 的正则模式。"""
    prefixes = "|".join(e.prefix for e in ALL_ENTITIES)
    return rf"(?:{prefixes})[_-]\d+"
