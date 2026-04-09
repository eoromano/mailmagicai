import re
from collections import Counter
from datetime import datetime, timezone
from typing import Optional

from app.schemas.common import EmailMessage, EmailThread
from app.schemas.responses import ThreadSummary, UserSettings
from app.services.triage_scoring import _extract_deadlines

REQUEST_OR_DECISION_PATTERN = re.compile(
    r"\b(review|approve|confirm|decide|reply|respond|share|send|need|waiting|blocker|follow up)\b",
    re.IGNORECASE,
)
QUESTION_PATTERN = re.compile(r"\?|\b(can you|could you|would you|do you|are you able)\b", re.IGNORECASE)


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _normalize_body(body: str) -> str:
    cleaned_lines: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(">"):
            continue
        if stripped.lower().startswith("from:"):
            continue
        if stripped.lower().startswith("sent from my"):
            continue
        cleaned_lines.append(stripped)
    return " ".join(cleaned_lines).strip()


def _sorted_messages(thread: EmailThread) -> list[EmailMessage]:
    return sorted(thread.messages, key=lambda message: _parse_timestamp(message.sent_at))


def _latest_message(thread: EmailThread) -> Optional[EmailMessage]:
    messages = _sorted_messages(thread)
    return messages[-1] if messages else None


def _sentence_split(text: str) -> list[str]:
    if not text:
        return []
    return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text) if sentence.strip()]


def _choose_summary_sentence(messages: list[EmailMessage]) -> str:
    scored_sentences: list[tuple[int, str]] = []
    for index, message in enumerate(messages):
        weight = index + 1
        for sentence in _sentence_split(_normalize_body(message.body_text)):
            score = weight
            if REQUEST_OR_DECISION_PATTERN.search(sentence):
                score += 3
            if QUESTION_PATTERN.search(sentence):
                score += 2
            if _extract_deadlines(sentence):
                score += 2
            scored_sentences.append((score, sentence))
    if not scored_sentences:
        return "No substantial message content was found in the thread."
    return max(scored_sentences, key=lambda item: item[0])[1]


def _collect_unresolved_items(messages: list[EmailMessage], settings: Optional[UserSettings]) -> list[str]:
    candidates: list[str] = []
    display_name = settings.display_name.lower() if settings else ""
    for message in reversed(messages):
        for sentence in _sentence_split(_normalize_body(message.body_text)):
            sentence_lower = sentence.lower()
            if REQUEST_OR_DECISION_PATTERN.search(sentence) or QUESTION_PATTERN.search(sentence):
                if display_name and display_name in sentence_lower:
                    candidates.append(sentence)
                else:
                    candidates.append(sentence)
    deduped: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        key = item.lower()
        if key not in seen:
            deduped.append(item)
            seen.add(key)
    return deduped[:3]


def _who_is_waiting(messages: list[EmailMessage], settings: Optional[UserSettings]) -> list[str]:
    waiting: list[str] = []
    display_name = settings.display_name if settings else "You"
    email = settings.email_address.lower() if settings and settings.email_address else None
    for message in reversed(messages):
        body = _normalize_body(message.body_text)
        body_lower = body.lower()
        sender = message.from_name
        if any(token in body_lower for token in ["waiting on", "blocker", "need", "follow up"]):
            if email and email in [recipient.lower() for recipient in message.to_recipients]:
                waiting.append(f"{sender} is waiting on {display_name} for a reply or decision.")
            elif display_name.lower() in body_lower:
                waiting.append(f"{sender} is waiting on {display_name} based on the latest message.")
    deduped: list[str] = []
    seen: set[str] = set()
    for item in waiting:
        if item not in seen:
            deduped.append(item)
            seen.add(item)
    return deduped[:3]


def _important_context(messages: list[EmailMessage]) -> list[str]:
    context_sentences: list[str] = []
    for message in messages[:-1]:
        for sentence in _sentence_split(_normalize_body(message.body_text)):
            if REQUEST_OR_DECISION_PATTERN.search(sentence) or _extract_deadlines(sentence):
                context_sentences.append(sentence)
    deduped: list[str] = []
    seen: set[str] = set()
    for sentence in context_sentences:
        key = sentence.lower()
        if key not in seen:
            deduped.append(sentence)
            seen.add(key)
    return deduped[:3]


def summarize_thread(thread: EmailThread, settings: Optional[UserSettings] = None) -> ThreadSummary:
    messages = _sorted_messages(thread)
    latest = _latest_message(thread)
    if not messages or latest is None:
        return ThreadSummary(
            summary="No useful message content was found in the thread.",
            latest_change="No latest update is available.",
            unresolved_items=[],
            who_is_waiting_on_whom=[],
            deadlines=[],
            important_context=[],
        )

    cleaned_latest = _normalize_body(latest.body_text)
    latest_sentences = _sentence_split(cleaned_latest)
    latest_change = latest_sentences[0] if latest_sentences else "No clear latest change found."

    deadlines: list[str] = []
    for message in messages:
        for deadline in _extract_deadlines(_normalize_body(message.body_text)):
            if deadline.lower() not in [existing.lower() for existing in deadlines]:
                deadlines.append(deadline)

    unresolved_items = _collect_unresolved_items(messages, settings)
    waiting = _who_is_waiting(messages, settings)
    context = _important_context(messages)

    summary_sentence = _choose_summary_sentence(messages)
    summary = summary_sentence
    if settings and settings.email_address:
        in_to_latest = settings.email_address.lower() in [recipient.lower() for recipient in latest.to_recipients]
        if in_to_latest:
            summary = f"{summary} You appear to be directly expected to respond."

    return ThreadSummary(
        summary=summary,
        latest_change=latest_change,
        unresolved_items=unresolved_items,
        who_is_waiting_on_whom=waiting,
        deadlines=deadlines,
        important_context=context,
    )
