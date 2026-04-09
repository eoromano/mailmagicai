from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from app.schemas.responses import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(status="ok", app_env=settings.app_env, mock_mode=settings.mock_mode)
