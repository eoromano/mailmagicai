from fastapi import APIRouter, Depends

from app.schemas.requests import ThreadRequest
from app.schemas.responses import TriageResult
from app.services import MockEmailTriageService

router = APIRouter(prefix="/triage", tags=["triage"])


def get_service() -> MockEmailTriageService:
    return MockEmailTriageService()


@router.post("/thread", response_model=TriageResult)
def triage_thread(
    request: ThreadRequest, service: MockEmailTriageService = Depends(get_service)
) -> TriageResult:
    return service.triage_thread(request.thread, request.user_settings)
