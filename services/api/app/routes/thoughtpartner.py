from fastapi import APIRouter, Depends

from app.schemas.requests import ThreadRequest
from app.schemas.responses import ThoughtPartnerResult
from app.services import MockEmailTriageService

router = APIRouter(tags=["thoughtpartner"])


def get_service() -> MockEmailTriageService:
    return MockEmailTriageService()


@router.post("/thoughtpartner", response_model=ThoughtPartnerResult)
def thoughtpartner(
    request: ThreadRequest, service: MockEmailTriageService = Depends(get_service)
) -> ThoughtPartnerResult:
    return service.thought_partner(request.thread, request.user_settings)
