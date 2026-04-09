from fastapi import APIRouter, Depends

from app.schemas.requests import CatchUpRequest
from app.schemas.responses import CatchUpOverview
from app.services import MockEmailTriageService, build_catchup_briefing
from app.services.fixtures import unread_threads_for_catchup

router = APIRouter(tags=["catchup"])


def get_service() -> MockEmailTriageService:
    return MockEmailTriageService()


@router.post("/catchup", response_model=CatchUpOverview)
def catchup(
    request: CatchUpRequest, service: MockEmailTriageService = Depends(get_service)
) -> CatchUpOverview:
    threads = request.threads or unread_threads_for_catchup()
    return service.features.catch_up_many(threads, request.user_settings)
