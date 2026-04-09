from datetime import datetime, timezone

from app.services.fixtures import (
    DEFAULT_USER_SETTINGS,
    thread_at_risk_of_being_missed,
    thread_copied_only,
    thread_important_fyi,
    thread_likely_needs_reply,
    thread_low_signal_noise,
    thread_needs_action_now,
)
from app.services.triage_scoring import choose_bucket, score_thread


def test_needs_action_now_bucket():
    score = score_thread(thread_needs_action_now(), DEFAULT_USER_SETTINGS, now=datetime(2026, 4, 8, tzinfo=timezone.utc))
    bucket, confidence = choose_bucket(score)
    assert bucket == "needs_action_now"
    assert confidence >= 0.7
    assert "5pm" in " ".join(score.detected_deadlines).lower()


def test_likely_needs_reply_bucket():
    score = score_thread(thread_likely_needs_reply(), DEFAULT_USER_SETTINGS, now=datetime(2026, 4, 8, tzinfo=timezone.utc))
    bucket, _ = choose_bucket(score)
    assert bucket == "likely_needs_reply"
    assert score.extracted_asks


def test_important_fyi_bucket():
    score = score_thread(thread_important_fyi(), DEFAULT_USER_SETTINGS, now=datetime(2026, 4, 8, tzinfo=timezone.utc))
    bucket, _ = choose_bucket(score)
    assert bucket == "important_fyi"


def test_copied_only_bucket():
    score = score_thread(thread_copied_only(), DEFAULT_USER_SETTINGS, now=datetime(2026, 4, 8, tzinfo=timezone.utc))
    bucket, _ = choose_bucket(score)
    assert bucket == "copied_only"


def test_low_signal_noise_bucket():
    score = score_thread(thread_low_signal_noise(), DEFAULT_USER_SETTINGS, now=datetime(2026, 4, 8, tzinfo=timezone.utc))
    bucket, _ = choose_bucket(score)
    assert bucket == "low_signal_noise"


def test_at_risk_of_being_missed_bucket():
    score = score_thread(
        thread_at_risk_of_being_missed(),
        DEFAULT_USER_SETTINGS,
        now=datetime(2026, 4, 9, tzinfo=timezone.utc),
    )
    bucket, _ = choose_bucket(score)
    assert bucket == "at_risk_of_being_missed"
