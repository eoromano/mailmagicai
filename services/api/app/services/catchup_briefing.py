from collections import Counter
from typing import Optional

from app.schemas.common import EmailThread
from app.schemas.responses import CatchUpBriefingItem, CatchUpBriefingOverview, CatchUpOverview, UserSettings
from typing import Protocol


class TriageServiceLike(Protocol):
    def build_triage_context(
        self, thread: EmailThread, settings: Optional[UserSettings] = None
    ) -> tuple[object, object, str, float, list[str], list[str]]: ...


def _dedupe_threads(threads: list[EmailThread]) -> list[EmailThread]:
    deduped: list[EmailThread] = []
    seen: set[str] = set()
    for thread in threads:
        latest_body = thread.messages[-1].body_text if thread.messages else ""
        key = f"{thread.subject.lower()}::{latest_body.strip().lower()}"
        if key not in seen:
            deduped.append(thread)
            seen.add(key)
    return deduped


def _to_briefing_item(service: TriageServiceLike, thread: EmailThread, settings: Optional[UserSettings]) -> CatchUpBriefingItem:
    summary, ask_result, bucket, _confidence, _detected_deadlines, top_reasons = service.build_triage_context(thread, settings)
    waiting_on_user = any("you" in reason.lower() or "user" in reason.lower() for reason in top_reasons) or bool(
        ask_result.asks
    )
    return CatchUpBriefingItem(
        id=f"brief-{thread.id}",
        thread_id=thread.id,
        subject=thread.subject,
        bucket=bucket,
        why_it_matters=top_reasons[0] if top_reasons else "This thread surfaced in triage.",
        latest_change=summary.latest_change,
        suggested_next_move=_suggested_next_move(bucket),
        waiting_on_user=waiting_on_user,
    )


def _suggested_next_move(bucket: str) -> str:
    return {
        "needs_action_now": "Reply with a short acknowledgment now, then resolve the open ask or deadline.",
        "likely_needs_reply": "Plan a reply soon and clarify the requested next step.",
        "important_fyi": "Scan the update, note anything important, and reply only if new risk appears.",
        "copied_only": "Monitor the thread, but do not interrupt your queue unless you are pulled in directly.",
        "low_signal_noise": "Archive or deprioritize the thread unless a new direct ask appears.",
        "at_risk_of_being_missed": "Re-read the thread and send a brief catch-up reply so it does not slip further.",
    }[bucket]


def _rank_item(item: CatchUpBriefingItem) -> tuple[int, int]:
    bucket_weight = {
        "needs_action_now": 6,
        "at_risk_of_being_missed": 5,
        "likely_needs_reply": 4,
        "important_fyi": 3,
        "copied_only": 2,
        "low_signal_noise": 1,
    }[item.bucket]
    waiting_bonus = 1 if item.waiting_on_user else 0
    return (bucket_weight, waiting_bonus)


def build_catchup_briefing(
    threads: list[EmailThread], service: TriageServiceLike, settings: Optional[UserSettings] = None
) -> CatchUpOverview:
    unique_threads = _dedupe_threads(threads)
    items = [_to_briefing_item(service, thread, settings) for thread in unique_threads]
    ranked_items = sorted(items, key=_rank_item, reverse=True)

    counts = Counter(item.bucket for item in ranked_items)
    overview = CatchUpBriefingOverview(
        total_items=len(ranked_items),
        needs_action_now_count=counts["needs_action_now"],
        likely_needs_reply_count=counts["likely_needs_reply"],
        important_fyi_count=counts["important_fyi"],
        copied_only_count=counts["copied_only"],
        low_signal_noise_count=counts["low_signal_noise"],
        at_risk_count=counts["at_risk_of_being_missed"],
    )

    themes: list[str] = []
    if counts["needs_action_now"] or counts["likely_needs_reply"]:
        themes.append("Several unread threads likely need a response from you.")
    if counts["at_risk_of_being_missed"]:
        themes.append("Older unread threads are at risk of slipping further.")
    if counts["important_fyi"]:
        themes.append("There are a few FYI items worth scanning for context.")

    return CatchUpOverview(
        overview=overview,
        top_action_items=[item for item in ranked_items if item.bucket in {"needs_action_now", "likely_needs_reply"}][:5],
        important_fyi_items=[item for item in ranked_items if item.bucket == "important_fyi"][:5],
        copied_only_items=[item for item in ranked_items if item.bucket == "copied_only"][:5],
        risk_items=[item for item in ranked_items if item.bucket in {"at_risk_of_being_missed", "needs_action_now"}][:5],
        themes=themes,
        suggested_first_10_to_read=ranked_items[:10],
    )
