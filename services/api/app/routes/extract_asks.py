from fastapi import APIRouter

from app.schemas.common import EmailThread
from app.schemas.responses import AskItem

router = APIRouter(prefix="/extract", tags=["extract"])


@router.post("/asks", response_model=list[AskItem])
def extract_asks(thread: EmailThread) -> list[AskItem]:
    return [
        AskItem(
            id="ask-placeholder-1",
            owner="You",
            request=f"Review open asks in '{thread.subject}'.",
        )
    ]
