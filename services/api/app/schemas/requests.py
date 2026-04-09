from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.common import EmailThread
from app.schemas.responses import UserSettings


class ThreadRequest(BaseModel):
    thread: EmailThread
    user_settings: Optional[UserSettings] = Field(default=None, alias="userSettings")

    model_config = {"populate_by_name": True}


class CatchUpRequest(BaseModel):
    threads: list[EmailThread] = Field(default_factory=list)
    user_settings: Optional[UserSettings] = Field(default=None, alias="userSettings")

    model_config = {"populate_by_name": True}
