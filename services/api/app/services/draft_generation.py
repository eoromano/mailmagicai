from typing import Optional

from app.schemas.common import EmailThread
from app.schemas.responses import AskExtractionResult, DraftReplySet, ThreadSummary, UserSettings


def _signature(user_settings: Optional[UserSettings]) -> str:
    return user_settings.signature if user_settings else "Thanks,\nYou"


def _first_deadline_value(deadlines: list[str]) -> str:
    return deadlines[0] if deadlines else "soon"


def generate_draft_replies(
    thread: EmailThread,
    summary: ThreadSummary,
    ask_result: AskExtractionResult,
    bucket: str,
    suggested_next_move: str,
    detected_deadlines: list[str],
    user_settings: Optional[UserSettings] = None,
) -> DraftReplySet:
    signature = _signature(user_settings)
    first_ask = ask_result.asks[0].text if ask_result.asks else suggested_next_move
    first_deadline = _first_deadline_value(detected_deadlines)
    unresolved = summary.unresolved_items[0] if summary.unresolved_items else "the remaining open point"
    latest_change = summary.latest_change.rstrip(".")

    short_reply = (
        f"Hi all,\n\nI am reviewing this now and will follow up on {unresolved} {first_deadline}."
        f"\n\n{signature}"
    )

    strategic_reply = (
        f"Hi all,\n\nI reviewed the thread and agree the next move should be: {suggested_next_move} "
        f"The latest change is that {latest_change.lower()}. I will take point on {first_ask.lower()}."
        f"\n\n{signature}"
    )

    clarifying_reply = (
        f"Hi all,\n\nBefore I lock a response, I want to clarify one point: {unresolved}. "
        f"Once that is confirmed, I can send the next update without overcommitting."
        f"\n\n{signature}"
    )

    return DraftReplySet(
        short_reply=short_reply,
        strategic_reply=strategic_reply,
        clarifying_reply=clarifying_reply,
        notes_on_when_to_use_each={
            "shortReply": "Use when you need to acknowledge quickly and buy time without adding commitments.",
            "strategicReply": "Use when you are ready to align the thread around a concrete next move.",
            "clarifyingReply": "Use when the thread is missing facts and a clarifying question is safer than committing.",
        },
    )
