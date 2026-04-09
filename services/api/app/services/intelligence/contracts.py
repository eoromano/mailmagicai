from typing import Optional

from pydantic import BaseModel, Field

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


class TriageFeatureInput(BaseModel):
    thread: EmailThread
    user_settings: Optional[UserSettings] = Field(default=None, alias="userSettings")

    model_config = {"populate_by_name": True}


class SummarizeFeatureInput(BaseModel):
    thread: EmailThread
    user_settings: Optional[UserSettings] = Field(default=None, alias="userSettings")

    model_config = {"populate_by_name": True}


class ExtractAsksFeatureInput(BaseModel):
    thread: EmailThread
    user_settings: Optional[UserSettings] = Field(default=None, alias="userSettings")

    model_config = {"populate_by_name": True}


class DraftReplyFeatureInput(BaseModel):
    thread: EmailThread
    summary: ThreadSummary
    ask_result: AskExtractionResult = Field(alias="askResult")
    triage_result: TriageResult = Field(alias="triageResult")
    user_settings: Optional[UserSettings] = Field(default=None, alias="userSettings")

    model_config = {"populate_by_name": True}


class CatchUpFeatureInput(BaseModel):
    threads: list[EmailThread]
    user_settings: Optional[UserSettings] = Field(default=None, alias="userSettings")

    model_config = {"populate_by_name": True}


class ThoughtPartnerFeatureInput(BaseModel):
    thread: EmailThread
    summary: ThreadSummary
    ask_result: AskExtractionResult = Field(alias="askResult")
    triage_result: TriageResult = Field(alias="triageResult")
    user_settings: Optional[UserSettings] = Field(default=None, alias="userSettings")

    model_config = {"populate_by_name": True}


class TriageFeatureOutput(TriageResult):
    pass


class SummarizeFeatureOutput(ThreadSummary):
    pass


class ExtractAsksFeatureOutput(AskExtractionResult):
    pass


class DraftReplyFeatureOutput(DraftReplySet):
    pass


class CatchUpFeatureOutput(CatchUpOverview):
    pass


class ThoughtPartnerFeatureOutput(ThoughtPartnerResult):
    pass
