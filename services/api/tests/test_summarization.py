from app.services.fixtures import DEFAULT_USER_SETTINGS, thread_for_summary_exec, thread_for_summary_repeated_quotes
from app.services.summarization import summarize_thread


def test_executive_summary_shape_is_populated():
    result = summarize_thread(thread_for_summary_exec(), DEFAULT_USER_SETTINGS)
    assert result.summary
    assert "respond" in result.summary.lower() or "you appear" in result.summary.lower()
    assert result.latest_change
    assert result.unresolved_items
    assert result.who_is_waiting_on_whom
    assert "today" in " ".join(result.deadlines).lower()
    assert result.important_context


def test_repeated_quotes_are_removed_from_latest_change():
    result = summarize_thread(thread_for_summary_repeated_quotes(), DEFAULT_USER_SETTINGS)
    assert "Earlier thread below" not in result.latest_change
    assert "Status update: launch checklist is complete." not in result.latest_change
    assert "customer note went out successfully" in result.latest_change.lower()
