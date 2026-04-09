import re
from typing import Optional

from app.schemas.common import EmailMessage, EmailThread
from app.schemas.responses import AskExtractionResult, AskType, AskUrgency, ExtractedAsk, UserSettings

EXPLICIT_ASK_PATTERNS: list[tuple[AskType, re.Pattern[str]]] = [
    ("approve", re.compile(r"\bapprove\b", re.IGNORECASE)),
    ("review", re.compile(r"\breview\b", re.IGNORECASE)),
    ("decide", re.compile(r"\bdecide\b", re.IGNORECASE)),
    ("confirm", re.compile(r"\bconfirm\b", re.IGNORECASE)),
    ("reply", re.compile(r"\b(reply|respond|get back)\b", re.IGNORECASE)),
    ("attend", re.compile(r"\b(join|attend|be there)\b", re.IGNORECASE)),
    ("delegate", re.compile(r"\b(find an owner|assign|delegate)\b", re.IGNORECASE)),
    ("provide_input", re.compile(r"\bshare|send|provide|input|feedback\b", re.IGNORECASE)),
]
QUESTION_PATTERN = re.compile(r"\?|\b(can you|could you|would you|please)\b", re.IGNORECASE)
WAITING_PATTERN = re.compile(r"\b(waiting on|blocker|blocked|holding on|need .* before)\b", re.IGNORECASE)
MISSING_REPLY_PATTERN = re.compile(r"\b(following up|checking in|haven't heard|still waiting|bumping this)\b", re.IGNORECASE)
DEADLINE_PATTERN = re.compile(
    r"\b(today|tomorrow|eod|end of day|asap|(?:by|before)\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)?|monday|tuesday|wednesday|thursday|friday)\b",
    re.IGNORECASE,
)


def _normalize_sentence(sentence: str) -> str:
    return re.sub(r"\s+", " ", sentence.strip())


def _split_sentences(text: str) -> list[str]:
    return [_normalize_sentence(part) for part in re.split(r"(?<=[.!?])\s+", text) if _normalize_sentence(part)]


def _infer_owner(message: EmailMessage, settings: Optional[UserSettings]) -> str:
    if settings:
        return settings.display_name
    return "You"


def _infer_target_person(message: EmailMessage) -> Optional[str]:
    return message.from_name if message.from_name else None


def _classify_ask_type(sentence: str) -> AskType:
    for ask_type, pattern in EXPLICIT_ASK_PATTERNS:
        if pattern.search(sentence):
            return ask_type
    if QUESTION_PATTERN.search(sentence):
        return "reply"
    return "no_action"


def _classify_ask_types(sentence: str) -> list[AskType]:
    matched: list[AskType] = []
    for ask_type, pattern in EXPLICIT_ASK_PATTERNS:
        if pattern.search(sentence):
            matched.append(ask_type)
    if not matched and QUESTION_PATTERN.search(sentence):
        matched.append("reply")
    return matched or ["no_action"]


def _infer_urgency(due_date: Optional[str], sentence: str) -> AskUrgency:
    if due_date or re.search(r"\b(asap|urgent|today|now)\b", sentence, re.IGNORECASE):
        return "high"
    if re.search(r"\b(this week|soon|follow up)\b", sentence, re.IGNORECASE):
        return "medium"
    return "low"


def _extract_deadlines(text: str) -> list[str]:
    matches = DEADLINE_PATTERN.findall(text)
    normalized: list[str] = []
    for match in matches:
        if match.lower() not in [item.lower() for item in normalized]:
            normalized.append(match)
    return normalized


def _build_asks(
    message: EmailMessage, sentence: str, index: int, settings: Optional[UserSettings]
) -> list[ExtractedAsk]:
    ask_types = _classify_ask_types(sentence)
    if ask_types == ["no_action"] and not QUESTION_PATTERN.search(sentence):
        return []

    deadlines = _extract_deadlines(sentence)
    due_date = deadlines[0] if deadlines else None
    asks: list[ExtractedAsk] = []
    for offset, ask_type in enumerate(ask_types):
        asks.append(
            ExtractedAsk(
                id=f"ask-{message.id}-{index + 1}-{offset + 1}",
                text=sentence,
                ask_type=ask_type,
                owner=_infer_owner(message, settings),
                target_person=_infer_target_person(message),
                due_date=due_date,
                urgency=_infer_urgency(due_date, sentence),
                source_snippet=sentence[:180],
            )
        )
    return asks


def extract_asks_from_thread(thread: EmailThread, settings: Optional[UserSettings] = None) -> AskExtractionResult:
    asks: list[ExtractedAsk] = []
    inferred_missing_replies: list[str] = []
    inferred_blockers: list[str] = []

    for message in sorted(thread.messages, key=lambda item: item.sent_at, reverse=True):
        for index, sentence in enumerate(_split_sentences(message.body_text)):
            asks.extend(_build_asks(message, sentence, index, settings))

            if MISSING_REPLY_PATTERN.search(sentence):
                inferred_missing_replies.append(f"{message.from_name} appears to be following up without a reply: {sentence}")

            if WAITING_PATTERN.search(sentence):
                inferred_blockers.append(f"{message.from_name} indicates a blocker: {sentence}")

    deduped_asks: list[ExtractedAsk] = []
    seen_text: set[str] = set()
    for ask in asks:
        key = f"{ask.text.lower()}::{ask.ask_type}"
        if key not in seen_text:
            deduped_asks.append(ask)
            seen_text.add(key)

    return AskExtractionResult(
        asks=deduped_asks[:5],
        inferred_missing_replies=list(dict.fromkeys(inferred_missing_replies))[:3],
        inferred_blockers=list(dict.fromkeys(inferred_blockers))[:3],
    )
