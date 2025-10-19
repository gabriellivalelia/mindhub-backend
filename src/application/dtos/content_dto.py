from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from domain.content import Content


class ContentDTO(BaseModel):
    id: UUID
    title: str
    body: str
    author_id: UUID
    created_at: datetime

    @staticmethod
    def to_dto(content: Content) -> "ContentDTO":
        return ContentDTO(
            id=content.id.value,
            title=content.title,
            body=content.body,
            author_id=content.author_id.value,
            created_at=content.created_at,
        )
