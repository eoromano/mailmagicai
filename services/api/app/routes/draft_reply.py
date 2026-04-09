from fastapi import APIRouter

from app.schemas.common import EmailThread

router = APIRouter(prefix="/draft", tags=["draft"])


@router.post("/reply", response_model=dict[str, str])
def draft_reply(thread: EmailThread) -> dict[str, str]:
    return {
        "draft": (
            f"Hi all,\n\nI reviewed '{thread.subject}' and will send a fuller response soon."
            "\n\nThanks,\nYou"
        )
    }
