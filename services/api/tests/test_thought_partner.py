from app.services.fixtures import DEFAULT_USER_SETTINGS, thread_for_summary_exec
from app.services.mock_email_triage_service import MockEmailTriageService


def test_thought_partner_returns_structured_analysis():
    result = MockEmailTriageService().thought_partner(thread_for_summary_exec())

    assert result.issue.evidence
    assert result.issue.inference
    assert result.explicit_asks
    assert result.implicit_dynamics.evidence
    assert result.implicit_dynamics.inference
    assert result.risks
    assert result.options
    assert result.recommended_move
    assert result.confidence_notes


def test_thought_partner_recommended_move_is_grounded_in_triage_direction():
    service = MockEmailTriageService()
    triage = service.triage_thread(thread_for_summary_exec(), DEFAULT_USER_SETTINGS)
    result = service.thought_partner(thread_for_summary_exec())

    assert triage.suggested_next_move.lower().split(".")[0] in result.recommended_move.lower()
