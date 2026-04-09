from app.services.ask_extraction import extract_asks_from_thread
from app.services.fixtures import (
    DEFAULT_USER_SETTINGS,
    thread_for_ask_extraction_explicit,
    thread_for_ask_extraction_implicit,
)


def test_explicit_asks_are_extracted_with_types_and_due_dates():
    result = extract_asks_from_thread(thread_for_ask_extraction_explicit(), DEFAULT_USER_SETTINGS)

    assert len(result.asks) >= 2
    assert any(ask.ask_type == "review" for ask in result.asks)
    assert any(ask.ask_type == "approve" for ask in result.asks)
    assert any((ask.due_date or "").lower().endswith("today") or "5pm" in (ask.due_date or "").lower() for ask in result.asks)
    assert any(ask.urgency == "high" for ask in result.asks)


def test_implicit_asks_and_blockers_are_inferred():
    result = extract_asks_from_thread(thread_for_ask_extraction_implicit(), DEFAULT_USER_SETTINGS)

    assert any(ask.ask_type == "decide" for ask in result.asks)
    assert result.inferred_missing_replies
    assert result.inferred_blockers
    assert any("blocked" in blocker.lower() for blocker in result.inferred_blockers)
