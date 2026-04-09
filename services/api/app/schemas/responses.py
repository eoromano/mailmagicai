from pydantic import BaseModel, Field


class SummaryResponse(BaseModel):
    overview: str
    bullets: list[str]


class AskItem(BaseModel):
    id: str
    owner: str
    request: str


class CatchUpItem(BaseModel):
    id: str
    title: str
    detail: str


class TriageResponse(BaseModel):
    thread_id: str = Field(alias="threadId")
    verdict: str
    rationale: str
    summary: SummaryResponse
    direct_asks: list[AskItem] = Field(alias="directAsks")
    draft_reply: str = Field(alias="draftReply")
    catch_up_list: list[CatchUpItem] = Field(alias="catchUpList")

    model_config = {"populate_by_name": True}
