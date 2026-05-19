"""Single source of truth for PRD Helper slash commands."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandSpec:
    name: str
    stage: str
    zh_description: str
    en_description: str
    outputs: str
    generated: bool = True

    @property
    def slash(self) -> str:
        return f"/{self.name}"

    @property
    def action(self) -> str:
        return self.name.removeprefix("prd-")


ALL_COMMANDS: tuple[CommandSpec, ...] = (
    CommandSpec(
        name="prd-helper",
        stage="初始化入口",
        zh_description="初始化或修复 PRD Helper 项目配置",
        en_description="Initialize or repair the current project configuration",
        outputs="配置、目录、Agent 规则",
        generated=False,
    ),
    CommandSpec(
        name="prd-start",
        stage="采集",
        zh_description="开启 PRD Helper 主动采集",
        en_description="Start PRD Helper active capture",
        outputs="01-collect/active/、collect-state.md",
    ),
    CommandSpec(
        name="prd-stop",
        stage="采集",
        zh_description="停止 PRD Helper 主动采集并生成摘要",
        en_description="Stop PRD Helper active capture and write summary output",
        outputs="collect-summary.md、01-collect/check.md",
    ),
    CommandSpec(
        name="prd-status",
        stage="采集工具",
        zh_description="查看 PRD Helper 采集状态",
        en_description="Show PRD Helper capture status",
        outputs="状态摘要",
    ),
    CommandSpec(
        name="prd-scan",
        stage="采集工具",
        zh_description="扫描所有 AI 工具的项目 session 并批量采集",
        en_description="Scan project sessions from AI tools into the capture pool",
        outputs="01-collect/active/historical/、source-index.md",
    ),
    CommandSpec(
        name="prd-import",
        stage="采集工具",
        zh_description="导入第三方文件夹数据作为被动材料",
        en_description="Import a third-party folder as passive material",
        outputs="01-collect/passive/、source-index.md",
    ),
    CommandSpec(
        name="prd-refine",
        stage="精炼",
        zh_description="直接精炼采集材料（不强制要求先完成采集）",
        en_description="Refine collected materials without requiring a completed collect step",
        outputs="02-refine/",
    ),
    CommandSpec(
        name="prd-relate",
        stage="关联",
        zh_description="直接建立关联关系（不强制要求先完成精炼）",
        en_description="Build relations without requiring a completed refine step",
        outputs="03-relate/",
    ),
    CommandSpec(
        name="prd-generate",
        stage="生成",
        zh_description="直接生成 PRD 文档（不强制要求先完成关联）",
        en_description="Generate PRD docs without requiring a completed relate step",
        outputs="04-generate/",
    ),
    CommandSpec(
        name="prd-discuss",
        stage="辅助研讨",
        zh_description="开启需求研讨模式 — 追问矛盾、模糊术语和未决问题",
        en_description="Discuss contradictions, vague terms, and unresolved questions",
        outputs="研讨摘要、待确认项",
    ),
    CommandSpec(
        name="prd-remove",
        stage="卸载",
        zh_description="卸载 PRD Helper 并清理 Agent 配置",
        en_description="Uninstall PRD Helper and clean Agent config",
        outputs="清理结果",
    ),
)

COMMAND_BY_NAME: dict[str, CommandSpec] = {command.name: command for command in ALL_COMMANDS}
GENERATED_COMMANDS: tuple[CommandSpec, ...] = tuple(command for command in ALL_COMMANDS if command.generated)
ALL_COMMAND_NAMES: tuple[str, ...] = tuple(command.name for command in ALL_COMMANDS)
GENERATED_COMMAND_NAMES: tuple[str, ...] = tuple(command.name for command in GENERATED_COMMANDS)


def command_by_name(name: str) -> CommandSpec:
    try:
        return COMMAND_BY_NAME[name]
    except KeyError:
        raise KeyError(f"Unknown command: {name}. Known: {sorted(COMMAND_BY_NAME)}") from None


def command_markdown_list(commands: tuple[CommandSpec, ...] = GENERATED_COMMANDS) -> str:
    return "\n".join(f"- `{command.slash}`：{command.zh_description}" for command in commands)
