from pydantic import BaseModel, Field
from typing import Optional


class EmailMessage(BaseModel):
    id: str
    from_name: str = Field(alias="fromName")
    from_email: str = Field(alias="fromEmail")
    to_recipients: list[str] = Field(default_factory=list, alias="toRecipients")
    cc_recipients: list[str] = Field(default_factory=list, alias="ccRecipients")
    sent_at: str = Field(alias="sentAt")
    body_text: str = Field(alias="bodyText")
    is_unread: bool = Field(alias="isUnread")

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
