from app.services.ask_extraction import extract_asks_from_thread
from app.services.draft_generation import generate_draft_replies
from app.services.fixtures import DEFAULT_USER_SETTINGS, thread_for_draft_generation
from app.services.mock_email_triage_service import MockEmailTriageService
from app.services.summarization import summarize_thread


def test_draft_generation_returns_three_distinct_options():
    thread = thread_for_draft_generation()
    summary = summarize_thread(thread, DEFAULT_USER_SETTINGS)
    ask_result = extract_asks_from_thread(thread, DEFAULT_USER_SETTINGS)
    triage = MockEmailTriageService().triage_thread(thread, DEFAULT_USER_SETTINGS)

    draft_set = generate_draft_replies(
        thread,
        summary,
        ask_result,
        triage.bucket,
        triage.suggested_next_move,
        triage.detected_deadlines,
        DEFAULT_USER_SETTINGS,
    )

    assert draft_set.short_reply != draft_set.strategic_reply
    assert draft_set.short_reply != draft_set.clarifying_reply
    assert draft_set.strategic_reply != draft_set.clarifying_reply
    assert "shortReply" in draft_set.notes_on_when_to_use_each
    assert "strategicReply" in draft_set.notes_on_when_to_use_each
    assert "clarifyingReply" in draft_set.notes_on_when_to_use_each


def test_mock_service_draft_reply_uses_template_strategy():
    draft_set = MockEmailTriageService().draft_reply(thread_for_draft_generation(), DEFAULT_USER_SETTINGS)
    assert "Hi all" in draft_set.short_reply
    assert "next move" in draft_set.strategic_reply.lower() or "reviewed the thread" in draft_set.strategic_reply.lower()
    assert "clarify" in draft_set.clarifying_reply.lower() or "confirm" in draft_set.clarifying_reply.lower()
