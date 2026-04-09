from typing import Optional

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
from app.services.intelligence import IntelligenceFeatureService


class MockEmailTriageService:
    """Deterministic mock implementation for local development."""

    def __init__(self):
        self.features = IntelligenceFeatureService()

    def _build_triage_context(
        self, thread: EmailThread, user_settings: Optional[UserSettings] = None
    ) -> tuple[ThreadSummary, AskExtractionResult, str, float, list[str], list[str]]:
        return self.features.build_triage_context(thread, user_settings)

    def build_triage_context(
        self, thread: EmailThread, user_settings: Optional[UserSettings] = None
    ) -> tuple[ThreadSummary, AskExtractionResult, str, float, list[str], list[str]]:
        return self._build_triage_context(thread, user_settings)

    def summarize_thread(self, thread: EmailThread, user_settings: Optional[UserSettings] = None) -> ThreadSummary:
        return self.features.summarize(thread, user_settings)

    def extract_asks(self, thread: EmailThread, user_settings: Optional[UserSettings] = None) -> AskExtractionResult:
        return self.features.extract_asks(thread, user_settings)

    def draft_reply(self, thread: EmailThread, user_settings: Optional[UserSettings] = None) -> DraftReplySet:
        return self.features.draft_reply(thread, user_settings)

    def catch_up(self, thread: EmailThread, user_settings: Optional[UserSettings] = None) -> CatchUpOverview:
        return self.features.catch_up(thread, user_settings)

    def thought_partner(
        self, thread: EmailThread, user_settings: Optional[UserSettings] = None
    ) -> ThoughtPartnerResult:
        return self.features.thought_partner(thread, user_settings)

    def triage_thread(self, thread: EmailThread, user_settings: Optional[UserSettings] = None) -> TriageResult:
        return self.features.triage_thread(thread, user_settings)
