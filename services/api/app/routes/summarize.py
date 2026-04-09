from fastapi import APIRouter, Depends

from app.schemas.requests import ThreadRequest
from app.schemas.responses import ThreadSummary
from app.services import MockEmailTriageService

router = APIRouter(prefix="/summarize", tags=["summarize"])


def get_service() -> MockEmailTriageService:
    return MockEmailTriageService()


@router.post("/thread", response_model=ThreadSummary)
def summarize_thread(
    request: ThreadRequest, service: MockEmailTriageService = Depends(get_service)
) -> ThreadSummary:
    return service.summarize_thread(request.thread, request.user_settings)
