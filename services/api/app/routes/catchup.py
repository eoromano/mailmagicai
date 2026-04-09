from fastapi import APIRouter

from app.schemas.common import EmailThread
from app.schemas.responses import CatchUpItem

router = APIRouter(tags=["catchup"])


@router.post("/catchup", response_model=list[CatchUpItem])
def catchup(thread: EmailThread) -> list[CatchUpItem]:
    return [
        CatchUpItem(
            id="catchup-placeholder-1",
            title="Unread items remain",
            detail=f"Mock catch-up view for '{thread.subject}'.",
        )
    ]
