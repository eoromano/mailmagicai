from typing import Literal, Optional

from pydantic import BaseModel, Field


TriageBucket = Literal[
    "needs_action_now",
    "likely_needs_reply",
    "important_fyi",
    "copied_only",
    "low_signal_noise",
    "at_risk_of_being_missed",
]


class HealthResponse(BaseModel):
    status: str
    app_env: str = Field(alias="appEnv")
    mock_mode: bool = Field(alias="mockMode")

    model_config = {"populate_by_name": True}


class TriageReason(BaseModel):
    id: str
    title: str
    detail: str


AskType = Literal[
    "review",
    "approve",
    "decide",
    "reply",
    "confirm",
    "attend",
    "delegate",
    "provide_input",
    "no_action",
]

AskUrgency = Literal["high", "medium", "low"]


class ExtractedAsk(BaseModel):
    id: str
    text: str
    ask_type: AskType = Field(alias="askType")
    owner: str
    target_person: Optional[str] = Field(default=None, alias="targetPerson")
    due_date: Optional[str] = Field(default=None, alias="dueDate")
    urgency: AskUrgency
    source_snippet: str = Field(alias="sourceSnippet")

    model_config = {"populate_by_name": True}


class AskExtractionResult(BaseModel):
    asks: list[ExtractedAsk]
    inferred_missing_replies: list[str] = Field(alias="inferredMissingReplies")
    inferred_blockers: list[str] = Field(alias="inferredBlockers")

    model_config = {"populate_by_name": True}


class ThreadSummary(BaseModel):
    summary: str
    latest_change: str = Field(alias="latestChange")
    unresolved_items: list[str] = Field(alias="unresolvedItems")
    who_is_waiting_on_whom: list[str] = Field(alias="whoIsWaitingOnWhom")
    deadlines: list[str]
    important_context: list[str] = Field(alias="importantContext")

    model_config = {"populate_by_name": True}


class DraftReplySet(BaseModel):
    short_reply: str = Field(alias="shortReply")
    strategic_reply: str = Field(alias="strategicReply")
    clarifying_reply: str = Field(alias="clarifyingReply")
    notes_on_when_to_use_each: dict[str, str] = Field(alias="notesOnWhenToUseEach")

    model_config = {"populate_by_name": True}


class CatchUpItem(BaseModel):
    id: str
    title: str
    detail: str


class CatchUpBriefingOverview(BaseModel):
    total_items: int = Field(alias="totalItems")
    needs_action_now_count: int = Field(alias="needsActionNowCount")
    likely_needs_reply_count: int = Field(alias="likelyNeedsReplyCount")
    important_fyi_count: int = Field(alias="importantFyiCount")
    copied_only_count: int = Field(alias="copiedOnlyCount")
    low_signal_noise_count: int = Field(alias="lowSignalNoiseCount")
    at_risk_count: int = Field(alias="atRiskCount")

    model_config = {"populate_by_name": True}


class CatchUpBriefingItem(BaseModel):
    id: str
    thread_id: str = Field(alias="threadId")
    subject: str
    bucket: TriageBucket
    why_it_matters: str = Field(alias="whyItMatters")
    latest_change: str = Field(alias="latestChange")
    suggested_next_move: str = Field(alias="suggestedNextMove")
    waiting_on_user: bool = Field(alias="waitingOnUser")

    model_config = {"populate_by_name": True}


class CatchUpOverview(BaseModel):
    overview: CatchUpBriefingOverview
    top_action_items: list[CatchUpBriefingItem] = Field(alias="topActionItems")
    important_fyi_items: list[CatchUpBriefingItem] = Field(alias="importantFyiItems")
    copied_only_items: list[CatchUpBriefingItem] = Field(alias="copiedOnlyItems")
    risk_items: list[CatchUpBriefingItem] = Field(alias="riskItems")
    themes: list[str]
    suggested_first_10_to_read: list[CatchUpBriefingItem] = Field(alias="suggestedFirst10ToRead")

    model_config = {"populate_by_name": True}


class EvidenceInference(BaseModel):
    evidence: list[str]
    inference: str


class ThoughtPartnerResult(BaseModel):
    issue: EvidenceInference
    explicit_asks: list[str] = Field(alias="explicitAsks")
    implicit_dynamics: EvidenceInference = Field(alias="implicitDynamics")
    risks: list[str]
    options: list[str]
    recommended_move: str = Field(alias="recommendedMove")
    confidence_notes: str = Field(alias="confidenceNotes")

    model_config = {"populate_by_name": True}


class TriageResult(BaseModel):
    thread_id: str = Field(alias="threadId")
    bucket: TriageBucket
    confidence: float
    verdict: str
    top_reasons: list[str] = Field(alias="topReasons")
    summary: ThreadSummary
    extracted_asks: list[ExtractedAsk] = Field(alias="extractedAsks")
    detected_deadlines: list[str] = Field(alias="detectedDeadlines")
    suggested_next_move: str = Field(alias="suggestedNextMove")
    draft_reply_set: DraftReplySet = Field(alias="draftReplySet")
    catch_up_overview: CatchUpOverview = Field(alias="catchUpOverview")
    thought_partner: ThoughtPartnerResult = Field(alias="thoughtPartner")

    model_config = {"populate_by_name": True}


class UserSettings(BaseModel):
    display_name: str = Field(alias="displayName")
    email_address: Optional[str] = Field(default=None, alias="emailAddress")
    signature: str
    reply_tone: str = Field(alias="replyTone")
    include_draft_replies: bool = Field(alias="includeDraftReplies")
    show_thought_partner: bool = Field(alias="showThoughtPartner")
    vip_senders: list[str] = Field(default_factory=list, alias="vipSenders")
    priority_domains: list[str] = Field(default_factory=list, alias="priorityDomains")
    urgency_keywords: list[str] = Field(default_factory=list, alias="urgencyKeywords")
    copied_only_keywords: list[str] = Field(default_factory=list, alias="copiedOnlyKeywords")
    draft_voice_preferences: list[str] = Field(default_factory=list, alias="draftVoicePreferences")
    save_history: bool = Field(default=True, alias="saveHistory")
    mock_mode: bool = Field(default=True, alias="mockMode")

    model_config = {"populate_by_name": True}
