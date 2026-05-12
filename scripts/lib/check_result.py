"""Shared Soft Gate result model for PRD Helper checks."""

from __future__ import annotations

from dataclasses import dataclass


STATUS_LABELS = {
    "passed": "通过",
    "failed": "不通过",
    "limited": "受限生成",
}


@dataclass(frozen=True)
class CheckResult:
    stage: str
    status: str
    can_proceed: bool
    risks: tuple[str, ...] = ()
    pending: tuple[str, ...] = ()

    @classmethod
    def passed(cls, stage: str) -> "CheckResult":
        return cls(stage=stage, status="passed", can_proceed=True)

    @property
    def summary(self) -> str:
        return f"{self.stage}: {self.status}"

    @property
    def has_risk(self) -> bool:
        return bool(self.risks or self.pending)

    def to_meta(self) -> dict[str, str]:
        pending = [*self.risks, *self.pending]
        return {
            "检查状态": STATUS_LABELS.get(self.status, self.status),
            "待确认项": "; ".join(pending) if pending else "无",
        }
