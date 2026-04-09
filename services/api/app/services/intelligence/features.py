from typing import Optional

from app.prompts import (
    CATCHUP_PROMPT,
    DRAFT_REPLY_PROMPT,
    EXTRACT_ASKS_PROMPT,
    SUMMARIZE_THREAD_PROMPT,
    THOUGHT_PARTNER_PROMPT,
    TRIAGE_THREAD_PROMPT,
)
from app.schemas.common import EmailThread
from app.schemas.responses import (
    AskExtractionResult,
    CatchUpOverview,
    DraftReplySet,
    ThoughtPartnerResult,
    ThreadSummary,
    TriageResult,
    UserSettings,
)
from app.services.ask_extraction import extract_asks_from_thread
from app.services.catchup_briefing import build_catchup_briefing
from app.services.draft_generation import generate_draft_replies
from app.services.intelligence.contracts import (
    CatchUpFeatureInput,
    CatchUpFeatureOutput,
    DraftReplyFeatureInput,
    DraftReplyFeatureOutput,
    ExtractAsksFeatureInput,
    ExtractAsksFeatureOutput,
    SummarizeFeatureInput,
    SummarizeFeatureOutput,
    ThoughtPartnerFeatureInput,
    ThoughtPartnerFeatureOutput,
    TriageFeatureInput,
    TriageFeatureOutput,
)
from app.services.modeling import ModelClient, NullModelClient
from app.services.summarization import summarize_thread
from app.services.thought_partner import build_thought_partner_analysis
from app.services.triage_scoring import choose_bucket, score_thread


BUCKET_LABELS = {
    "needs_action_now": "Needs action now",
    "likely_needs_reply": "Likely needs reply",
    "important_fyi": "Important FYI",
    "copied_only": "Copied only",
    "low_signal_noise": "Low-signal noise",
    "at_risk_of_being_missed": "At risk of being missed",
}

NEXT_MOVE_MAP = {
    "needs_action_now": "Reply with a short acknowledgment now, then resolve the open ask or deadline.",
    "likely_needs_reply": "Plan a reply soon and clarify the requested next step.",
    "important_fyi": "Scan the update, note anything important, and reply only if new risk appears.",
    "copied_only": "Monitor the thread, but do not interrupt your queue unless you are pulled in directly.",
    "low_signal_noise": "Archive or deprioritize the thread unless a new direct ask appears.",
    "at_risk_of_being_missed": "Re-read the thread and send a brief catch-up reply so it does not slip further.",
}


class IntelligenceFeatureService:
    def __init__(self, model_client: Optional[ModelClient] = None):
        self.model_client = model_client or NullModelClient()

    def summarize(
        self, thread: EmailThread, user_settings: Optional[UserSettings] = None
    ) -> ThreadSummary:
        feature_input = SummarizeFeatureInput(thread=thread, userSettings=user_settings)
        model_result = self.model_client.generate_structured(
            feature_name="summarize",
            prompt=SUMMARIZE_THREAD_PROMPT,
            payload=feature_input,
            response_model=SummarizeFeatureOutput,
        )
        if model_result is not None:
            return model_result
        return summarize_thread(thread, user_settings)

    def extract_asks(
        self, thread: EmailThread, user_settings: Optional[UserSettings] = None
    ) -> AskExtractionResult:
        feature_input = ExtractAsksFeatureInput(thread=thread, userSettings=user_settings)
        model_result = self.model_client.generate_structured(
            feature_name="extract_asks",
            prompt=EXTRACT_ASKS_PROMPT,
            payload=feature_input,
            response_model=ExtractAsksFeatureOutput,
        )
        if model_result is not None:
            return model_result
        return extract_asks_from_thread(thread, user_settings)

    def build_triage_context(
        self, thread: EmailThread, user_settings: Optional[UserSettings] = None
    ) -> tuple[ThreadSummary, AskExtractionResult, str, float, list[str], list[str]]:
        summary = self.summarize(thread, user_settings)
        scored = score_thread(thread, user_settings)
        bucket, confidence = choose_bucket(scored)
        ask_result = self.extract_asks(thread, user_settings)
        top_reasons = scored.top_reasons[:3] or ["The thread was scored using default fallback rules."]
        return summary, ask_result, bucket, confidence, scored.detected_deadlines, top_reasons

    def triage_thread(
        self, thread: EmailThread, user_settings: Optional[UserSettings] = None
    ) -> TriageResult:
        summary, ask_result, bucket, confidence, detected_deadlines, top_reasons = self.build_triage_context(
            thread, user_settings
        )
        deterministic_result = TriageResult(
            thread_id=thread.id,
            bucket=bucket,
            confidence=confidence,
            verdict=BUCKET_LABELS[bucket],
            top_reasons=top_reasons,
            summary=summary,
            extracted_asks=ask_result.asks,
            detected_deadlines=detected_deadlines,
            suggested_next_move=NEXT_MOVE_MAP[bucket],
            draft_reply_set=self.draft_reply(thread, user_settings),
            catch_up_overview=self.catch_up(thread, user_settings),
            thought_partner=self.thought_partner(thread, user_settings),
        )
        feature_input = TriageFeatureInput(thread=thread, userSettings=user_settings)
        model_result = self.model_client.generate_structured(
            feature_name="triage",
            prompt=TRIAGE_THREAD_PROMPT,
            payload=feature_input,
            response_model=TriageFeatureOutput,
        )
        return model_result or deterministic_result

    def draft_reply(
        self, thread: EmailThread, user_settings: Optional[UserSettings] = None
    ) -> DraftReplySet:
        summary, ask_result, bucket, confidence, detected_deadlines, top_reasons = self.build_triage_context(
            thread, user_settings
        )
        _ = confidence, top_reasons
        triage_result = TriageResult(
            thread_id=thread.id,
            bucket=bucket,
            confidence=confidence,
            verdict=BUCKET_LABELS[bucket],
            top_reasons=top_reasons,
            summary=summary,
            extracted_asks=ask_result.asks,
            detected_deadlines=detected_deadlines,
            suggested_next_move=NEXT_MOVE_MAP[bucket],
            draft_reply_set=DraftReplySet(
                short_reply="",
                strategic_reply="",
                clarifying_reply="",
                notes_on_when_to_use_each={},
            ),
            catch_up_overview=CatchUpOverview(
                overview={"totalItems": 0, "needsActionNowCount": 0, "likelyNeedsReplyCount": 0, "importantFyiCount": 0, "copiedOnlyCount": 0, "lowSignalNoiseCount": 0, "atRiskCount": 0},
                topActionItems=[],
                importantFyiItems=[],
                copiedOnlyItems=[],
                riskItems=[],
                themes=[],
                suggestedFirst10ToRead=[],
            ),
            thought_partner=ThoughtPartnerResult(
                issue={"evidence": [], "inference": ""},
                explicitAsks=[],
                implicitDynamics={"evidence": [], "inference": ""},
                risks=[],
                options=[],
                recommendedMove="",
                confidenceNotes="",
            ),
        )
        deterministic_result = generate_draft_replies(
            thread,
            summary,
            ask_result,
            bucket,
            NEXT_MOVE_MAP[bucket],
            detected_deadlines,
            user_settings,
        )
        feature_input = DraftReplyFeatureInput(
            thread=thread,
            summary=summary,
            askResult=ask_result,
            triageResult=triage_result,
            userSettings=user_settings,
        )
        model_result = self.model_client.generate_structured(
            feature_name="draft_reply",
            prompt=DRAFT_REPLY_PROMPT,
            payload=feature_input,
            response_model=DraftReplyFeatureOutput,
        )
        return model_result or deterministic_result

    def catch_up(
        self, thread: EmailThread, user_settings: Optional[UserSettings] = None
    ) -> CatchUpOverview:
        deterministic_result = build_catchup_briefing([thread], self, user_settings)
        feature_input = CatchUpFeatureInput(threads=[thread], userSettings=user_settings)
        model_result = self.model_client.generate_structured(
            feature_name="catchup",
            prompt=CATCHUP_PROMPT,
            payload=feature_input,
            response_model=CatchUpFeatureOutput,
        )
        return model_result or deterministic_result

    def catch_up_many(
        self, threads: list[EmailThread], user_settings: Optional[UserSettings] = None
    ) -> CatchUpOverview:
        deterministic_result = build_catchup_briefing(threads, self, user_settings)
        feature_input = CatchUpFeatureInput(threads=threads, userSettings=user_settings)
        model_result = self.model_client.generate_structured(
            feature_name="catchup",
            prompt=CATCHUP_PROMPT,
            payload=feature_input,
            response_model=CatchUpFeatureOutput,
        )
        return model_result or deterministic_result

    def thought_partner(
        self, thread: EmailThread, user_settings: Optional[UserSettings] = None
    ) -> ThoughtPartnerResult:
        summary, ask_result, bucket, confidence, detected_deadlines, top_reasons = self.build_triage_context(
            thread, user_settings
        )
        deterministic_result = build_thought_partner_analysis(
            thread,
            summary,
            ask_result,
            bucket,
            top_reasons,
            detected_deadlines,
            NEXT_MOVE_MAP[bucket],
            user_settings,
        )
        triage_result = TriageResult(
            thread_id=thread.id,
            bucket=bucket,
            confidence=confidence,
            verdict=BUCKET_LABELS[bucket],
            top_reasons=top_reasons,
            summary=summary,
            extracted_asks=ask_result.asks,
            detected_deadlines=detected_deadlines,
            suggested_next_move=NEXT_MOVE_MAP[bucket],
            draft_reply_set=DraftReplySet(
                short_reply="",
                strategic_reply="",
                clarifying_reply="",
                notes_on_when_to_use_each={},
            ),
            catch_up_overview=CatchUpOverview(
                overview={"totalItems": 0, "needsActionNowCount": 0, "likelyNeedsReplyCount": 0, "importantFyiCount": 0, "copiedOnlyCount": 0, "lowSignalNoiseCount": 0, "atRiskCount": 0},
                topActionItems=[],
                importantFyiItems=[],
                copiedOnlyItems=[],
                riskItems=[],
                themes=[],
                suggestedFirst10ToRead=[],
            ),
            thought_partner=deterministic_result,
        )
        feature_input = ThoughtPartnerFeatureInput(
            thread=thread,
            summary=summary,
            askResult=ask_result,
            triageResult=triage_result,
            userSettings=user_settings,
        )
        model_result = self.model_client.generate_structured(
            feature_name="thought_partner",
            prompt=THOUGHT_PARTNER_PROMPT,
            payload=feature_input,
            response_model=ThoughtPartnerFeatureOutput,
        )
        return model_result or deterministic_result
