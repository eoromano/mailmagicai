from fastapi import APIRouter

from app.schemas.common import EmailThread
from app.schemas.responses import SummaryResponse

router = APIRouter(prefix="/summarize", tags=["summarize"])


@router.post("/thread", response_model=SummaryResponse)
def summarize_thread(thread: EmailThread) -> SummaryResponse:
    return SummaryResponse(
        overview=f"Mock summary for '{thread.subject}'.",
        bullets=[
            "This endpoint currently returns placeholder content.",
            "Real summarization logic will plug in later.",
        ],
    )
