from scripts.lib.check_result import CheckResult


def test_check_result_exposes_soft_gate_status_and_pending_items():
    result = CheckResult(
        stage="Generate",
        status="limited",
        can_proceed=False,
        risks=("02-refine/ 缺失",),
        pending=("补充 Strong Trace",),
    )

    assert result.summary == "Generate: limited"
    assert result.has_risk
    assert result.to_meta()["检查状态"] == "受限生成"
    assert "02-refine/ 缺失" in result.to_meta()["待确认项"]


def test_check_result_passed_result_has_no_pending_items():
    result = CheckResult.passed("Refine")

    assert result.can_proceed
    assert not result.has_risk
    assert result.to_meta()["检查状态"] == "通过"
    assert result.to_meta()["待确认项"] == "无"
