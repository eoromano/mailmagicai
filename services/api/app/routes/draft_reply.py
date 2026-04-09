from fastapi import APIRouter, Depends

from app.schemas.requests import ThreadRequest
from app.schemas.responses import DraftReplySet
from app.services import MockEmailTriageService

router = APIRouter(prefix="/draft", tags=["draft"])


def get_service() -> MockEmailTriageService:
    return MockEmailTriageService()


@router.post("/reply", response_model=DraftReplySet)
def draft_reply(
    request: ThreadRequest, service: MockEmailTriageService = Depends(get_service)
) -> DraftReplySet:
    return service.draft_reply(request.thread, request.user_settings)
