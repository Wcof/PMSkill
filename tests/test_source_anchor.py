from scripts.lib.source_anchor import trace_quality


def test_source_anchor_accepts_strong_trace_with_quote():
    block = "\n".join([
        "- source_id：turn-001",
        "- path：active/sessions/session-test.md",
        "- quote：用户要求巡检点位管理",
        "- locator：Turn 1",
    ])

    quality = trace_quality(block)

    assert quality.strong
    assert quality.missing == []


def test_source_anchor_rejects_missing_locator_as_weak_trace():
    block = "\n".join([
        "- source_id：turn-001",
        "- path：active/sessions/session-test.md",
        "- quote：用户要求巡检点位管理",
    ])

    quality = trace_quality(block)

    assert not quality.strong
    assert quality.missing == ["locator"]


def test_source_anchor_rejects_missing_quote_or_paraphrase():
    block = "\n".join([
        "- source_id：turn-001",
        "- path：active/sessions/session-test.md",
        "- locator：Turn 1",
    ])

    quality = trace_quality(block)

    assert not quality.strong
    assert quality.missing == ["quote/paraphrase"]


def test_source_anchor_supports_bilingual_quote_fields():
    block = "\n".join([
        "- source_id：turn-001",
        "- path：active/sessions/session-test.md",
        "- locator：Turn 1",
        "- 转述：用户描述了巡检需求",
    ])

    assert trace_quality(block).strong
