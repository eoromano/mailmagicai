import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from app.schemas.common import EmailMessage, EmailThread
from app.schemas.responses import ExtractedAsk, TriageBucket, UserSettings
from app.services.ask_extraction import extract_asks_from_thread

REQUEST_PATTERNS = re.compile(r"\b(review|approve|confirm|decide|reply|respond|share|send)\b", re.IGNORECASE)
QUESTION_PATTERNS = re.compile(r"\?|\b(can you|could you|would you|do you|are you able)\b", re.IGNORECASE)
DEADLINE_PATTERNS = re.compile(
    r"\b(today|tomorrow|eod|end of day|asap|(?:by|before)\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)?|monday|tuesday|wednesday|thursday|friday)\b",
    re.IGNORECASE,
)
AUTOMATED_PATTERNS = re.compile(r"\b(no-?reply|automated|notification|digest|alert|bot)\b", re.IGNORECASE)
STATUS_UPDATE_PATTERNS = re.compile(r"\b(fyi|for visibility|status update|weekly update|digest|summary)\b", re.IGNORECASE)


@dataclass
class SignalScore:
    bucket_scores: dict[TriageBucket, float] = field(
        default_factory=lambda: {
            "needs_action_now": 0.0,
            "likely_needs_reply": 0.0,
            "important_fyi": 0.0,
            "copied_only": 0.0,
            "low_signal_noise": 0.0,
            "at_risk_of_being_missed": 0.0,
        }
    )
    top_reasons: list[str] = field(default_factory=list)
    detected_deadlines: list[str] = field(default_factory=list)
    extracted_asks: list[ExtractedAsk] = field(default_factory=list)

    def add(self, bucket: TriageBucket, points: float, reason: Optional[str] = None) -> None:
        self.bucket_scores[bucket] += points
        if reason and reason not in self.top_reasons:
            self.top_reasons.append(reason)


def _parse_timestamp(value: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _latest_message(thread: EmailThread) -> Optional[EmailMessage]:
    if not thread.messages:
        return None
    return max(thread.messages, key=lambda message: message.sent_at)


def _user_mentions(message: EmailMessage, settings: Optional[UserSettings]) -> bool:
    if not settings:
        return False
    haystack = message.body_text.lower()
    if settings.display_name.lower() in haystack:
        return True
    if settings.email_address and settings.email_address.lower() in haystack:
        return True
    return False


def _is_user_in_to(message: EmailMessage, settings: Optional[UserSettings]) -> bool:
    if not settings or not settings.email_address:
        return False
    return settings.email_address.lower() in [recipient.lower() for recipient in message.to_recipients]


def _is_user_only_in_cc(message: EmailMessage, settings: Optional[UserSettings]) -> bool:
    if not settings or not settings.email_address:
        return False
    email = settings.email_address.lower()
    in_cc = email in [recipient.lower() for recipient in message.cc_recipients]
    in_to = email in [recipient.lower() for recipient in message.to_recipients]
    return in_cc and not in_to


def _extract_deadlines(text: str) -> list[str]:
    matches = DEADLINE_PATTERNS.findall(text)
    normalized: list[str] = []
    for match in matches:
        value = match.strip()
        if value.lower() not in [existing.lower() for existing in normalized]:
            normalized.append(value)
    return normalized


def score_thread(thread: EmailThread, settings: Optional[UserSettings], now: Optional[datetime] = None) -> SignalScore:
    now = now or datetime.now(timezone.utc)
    latest = _latest_message(thread)
    score = SignalScore()

    if latest is None:
        score.add("low_signal_noise", 1.0, "The thread has no message content to evaluate.")
        return score

    body = latest.body_text
    deadlines = _extract_deadlines(body)
    score.detected_deadlines.extend(deadlines)
    extracted_asks = extract_asks_from_thread(thread, settings).asks
    score.extracted_asks.extend(extracted_asks)

    user_in_to = _is_user_in_to(latest, settings)
    user_only_in_cc = _is_user_only_in_cc(latest, settings)
    user_explicitly_addressed = _user_mentions(latest, settings)
    has_question = bool(QUESTION_PATTERNS.search(body))
    has_request_language = bool(REQUEST_PATTERNS.search(body))
    has_urgent_request = bool(re.search(r"\b(approve|decide|confirm)\b", body, re.IGNORECASE))

    if user_in_to:
        score.add("likely_needs_reply", 1.2, "The user is directly in the To line.")
        if deadlines or has_urgent_request:
            score.add("needs_action_now", 0.8)

    if user_only_in_cc:
        score.add("copied_only", 2.0, "The user appears only in Cc.")
        score.add("important_fyi", 0.5)

    if has_question and not user_only_in_cc:
        score.add("likely_needs_reply", 1.1, "The latest message contains a direct question.")

    if has_request_language and not user_only_in_cc:
        score.add("likely_needs_reply", 0.9, "The message uses direct request language like review, approve, confirm, or decide.")
        if deadlines or has_urgent_request:
            score.add("needs_action_now", 1.1, "The thread combines a request with a timing or decision signal.")

    if deadlines:
        score.add("needs_action_now", 1.3, f"A deadline was detected: {', '.join(deadlines)}.")

    recipient_count = len(set(latest.to_recipients + latest.cc_recipients))
    is_status_update = bool(STATUS_UPDATE_PATTERNS.search(body))
    if recipient_count >= 6:
        score.add("important_fyi", 0.6, "The message was sent to a broad group.")
        score.add("low_signal_noise", 0.4)

    sender_and_body = f"{latest.from_name} {latest.from_email} {body}"
    if AUTOMATED_PATTERNS.search(sender_and_body):
        score.add("low_signal_noise", 1.7, "The message looks automated or system-generated.")

    if is_status_update and not extracted_asks:
        score.add("important_fyi", 1.6, "The message reads like a broad status update or FYI.")
        if user_only_in_cc:
            score.add("important_fyi", 0.8, "The user is copied for visibility on an FYI-style update.")

    if user_explicitly_addressed and not user_only_in_cc:
        score.add("likely_needs_reply", 0.7, "The message explicitly addresses the user.")

    if user_in_to and deadlines and has_urgent_request:
        score.add("needs_action_now", 1.4, "The thread asks the user for a decision on a deadline.")

    last_message_at = _parse_timestamp(thread.last_message_at)
    if last_message_at and thread.unread_count > 0:
        age_days = (now - last_message_at).days
        if age_days >= 5 and not AUTOMATED_PATTERNS.search(sender_and_body):
            score.add("at_risk_of_being_missed", 3.0, "The thread is older, still unread, and may be getting buried.")
            score.add("likely_needs_reply", 0.5)
            if re.search(r"\b(following up|buried|just checking in)\b", body, re.IGNORECASE):
                score.add("at_risk_of_being_missed", 1.4, "The sender is explicitly following up on an older unread thread.")

    if extracted_asks and score.bucket_scores["needs_action_now"] < 2.0:
        score.add("likely_needs_reply", 0.5, "The thread includes at least one explicit ask.")

    if score.bucket_scores["low_signal_noise"] >= 1.7 and not extracted_asks:
        score.add("low_signal_noise", 0.4, "No direct ask was detected.")

    return score


def choose_bucket(score: SignalScore) -> tuple[TriageBucket, float]:
    ordered = sorted(score.bucket_scores.items(), key=lambda item: item[1], reverse=True)
    winner, winner_score = ordered[0]
    runner_up_score = ordered[1][1] if len(ordered) > 1 else 0.0

    at_risk_score = score.bucket_scores["at_risk_of_being_missed"]
    if at_risk_score >= 4.0 and winner != "at_risk_of_being_missed" and winner_score - at_risk_score <= 0.75:
        winner = "at_risk_of_being_missed"
        winner_score = at_risk_score

    low_signal_score = score.bucket_scores["low_signal_noise"]
    if (
        low_signal_score >= 2.0
        and not score.extracted_asks
        and winner != "low_signal_noise"
        and winner_score - low_signal_score <= 1.0
    ):
        winner = "low_signal_noise"
        winner_score = low_signal_score

    confidence = 0.55 if winner_score <= 0 else min(0.99, 0.55 + (winner_score - runner_up_score) / 4)
    return winner, round(confidence, 2)
