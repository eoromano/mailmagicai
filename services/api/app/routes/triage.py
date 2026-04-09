from fastapi import APIRouter

from app.schemas.common import EmailThread
from app.schemas.responses import AskItem, CatchUpItem, SummaryResponse, TriageResponse

router = APIRouter(prefix="/triage", tags=["triage"])


@router.post("/thread", response_model=TriageResponse)
def triage_thread(thread: EmailThread) -> TriageResponse:
    return TriageResponse(
        thread_id=thread.id,
        verdict="Needs reply today",
        rationale="Mock triage result for early UI and API integration.",
        summary=SummaryResponse(
            overview=f"Thread '{thread.subject}' is waiting on a clear owner and reply.",
            bullets=[
                "This is placeholder logic.",
                "Use this endpoint to wire the frontend safely before model integration.",
            ],
        ),
        direct_asks=[
            AskItem(
                id="ask-placeholder-1",
                owner="You",
                request="Review the thread and confirm the next action.",
            )
        ],
        draft_reply="Hi team,\n\nI reviewed the thread and will follow up shortly.\n\nThanks,\nYou",
        catch_up_list=[
            CatchUpItem(
                id="catchup-placeholder-1",
                title="Pending decision",
                detail="A follow-up decision is still open in this thread.",
            )
        ],
    )
