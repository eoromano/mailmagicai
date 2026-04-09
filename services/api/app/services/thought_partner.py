from typing import Optional

from app.schemas.common import EmailThread
from app.schemas.responses import AskExtractionResult, EvidenceInference, ThoughtPartnerResult, ThreadSummary, UserSettings


def build_thought_partner_analysis(
    thread: EmailThread,
    summary: ThreadSummary,
    ask_result: AskExtractionResult,
    bucket: str,
    top_reasons: list[str],
    detected_deadlines: list[str],
    suggested_next_move: str,
    user_settings: Optional[UserSettings] = None,
) -> ThoughtPartnerResult:
    display_name = user_settings.display_name if user_settings else "You"

    issue_evidence = []
    if summary.latest_change:
        issue_evidence.append(summary.latest_change)
    issue_evidence.extend(summary.unresolved_items[:2])
    if top_reasons:
        issue_evidence.extend(top_reasons[:2])

    issue_inference = (
        "The real issue is that the thread needs a concrete decision and a clear owner before others can move."
        if bucket in {"needs_action_now", "likely_needs_reply"}
        else "The real issue is mainly context management rather than an urgent action."
    )

    explicit_asks = [ask.text for ask in ask_result.asks[:4]]
    if not explicit_asks:
        explicit_asks = summary.unresolved_items[:2]

    dynamic_evidence = []
    dynamic_evidence.extend(summary.who_is_waiting_on_whom[:2])
    dynamic_evidence.extend(ask_result.inferred_blockers[:2])
    if not dynamic_evidence and top_reasons:
        dynamic_evidence.extend(top_reasons[:2])

    if any("waiting" in item.lower() or "blocked" in item.lower() for item in dynamic_evidence):
        implicit_inference = (
            f"Stakeholders appear to be waiting on {display_name} for a decision or response, which raises coordination pressure."
        )
    else:
        implicit_inference = "The thread suggests moderate coordination pressure, but no single stakeholder dependency is fully explicit."

    risks = []
    if bucket in {"needs_action_now", "likely_needs_reply", "at_risk_of_being_missed"}:
        risks.append("If you do nothing, other people may stay blocked and the thread may continue to escalate.")
    if detected_deadlines:
        risks.append(f"If you wait too long, you may miss the timing signal around {', '.join(detected_deadlines[:2])}.")
    if ask_result.inferred_missing_replies:
        risks.append("There are signs the sender already feels this thread has gone unanswered.")
    if not risks:
        risks.append("The main risk is losing useful context if the thread keeps growing without a decision.")

    options = [
        f"Send a short acknowledgment that buys time while keeping ownership clear for {display_name}.",
        f"Act on the main ask directly: {suggested_next_move}",
        "Ask one clarifying question if the thread still lacks a safe basis for a commitment.",
    ]

    recommended_move = suggested_next_move
    confidence_notes = (
        "High confidence on the explicit asks and practical next move because they are supported directly by the latest thread content. "
        "Any stakeholder-motive inference is lower confidence because intent is inferred from phrasing and blocking language."
    )

    return ThoughtPartnerResult(
        issue=EvidenceInference(evidence=issue_evidence[:3], inference=issue_inference),
        explicit_asks=explicit_asks,
        implicit_dynamics=EvidenceInference(evidence=dynamic_evidence[:3], inference=implicit_inference),
        risks=risks[:3],
        options=options,
        recommended_move=recommended_move,
        confidence_notes=confidence_notes,
    )
