from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from domain.content import Content


class AuthorDTO(BaseModel):
    id: UUID
    name: str


class ContentDTO(BaseModel):
    id: UUID
    title: str
    body: str
    author_id: UUID
    author: AuthorDTO | None = None
    created_at: datetime

    @staticmethod
    def to_dto(content: Content, author_name: str | None = None) -> "ContentDTO":
        author_dto = None
        if author_name:
            author_dto = AuthorDTO(id=content.author_id.value, name=author_name)

        return ContentDTO(
            id=content.id.value,
            title=content.title,
            body=content.body,
            author_id=content.author_id.value,
            author=author_dto,
            created_at=content.created_at,
        )
