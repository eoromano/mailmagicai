from app.services import MockEmailTriageService, build_catchup_briefing
from app.services.fixtures import DEFAULT_USER_SETTINGS, unread_threads_for_catchup


def test_catchup_briefing_counts_and_lists_are_populated():
    briefing = build_catchup_briefing(unread_threads_for_catchup(), MockEmailTriageService(), DEFAULT_USER_SETTINGS)

    assert briefing.overview.total_items >= 6
    assert briefing.overview.needs_action_now_count >= 1
    assert briefing.top_action_items
    assert briefing.suggested_first_10_to_read


def test_catchup_briefing_ranks_action_and_risk_near_top():
    briefing = build_catchup_briefing(unread_threads_for_catchup(), MockEmailTriageService(), DEFAULT_USER_SETTINGS)

    first_two_buckets = [item.bucket for item in briefing.suggested_first_10_to_read[:2]]
    assert any(bucket in {"needs_action_now", "at_risk_of_being_missed"} for bucket in first_two_buckets)
    assert briefing.themes
