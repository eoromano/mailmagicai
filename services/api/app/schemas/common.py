from pydantic import BaseModel, Field


class EmailMessage(BaseModel):
    id: str
    from_: str = Field(alias="from")
    sent_at: str = Field(alias="sentAt")
    body: str

    model_config = {"populate_by_name": True}


class EmailThread(BaseModel):
    id: str
    subject: str
    participants: list[str]
    message_count: int = Field(alias="messageCount")
    unread_count: int = Field(alias="unreadCount")
    last_message_at: str = Field(alias="lastMessageAt")
    messages: list[EmailMessage]

    model_config = {"populate_by_name": True}
