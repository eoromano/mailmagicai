from fastapi import APIRouter, Depends

from app.schemas.requests import ThreadRequest
from app.schemas.responses import AskExtractionResult
from app.services import MockEmailTriageService

router = APIRouter(prefix="/extract", tags=["extract"])


def get_service() -> MockEmailTriageService:
    return MockEmailTriageService()


@router.post("/asks", response_model=AskExtractionResult)
def extract_asks(
    request: ThreadRequest, service: MockEmailTriageService = Depends(get_service)
) -> AskExtractionResult:
    return service.extract_asks(request.thread, request.user_settings)
