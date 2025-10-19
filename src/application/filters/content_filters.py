from uuid import UUID

from pydantic import BaseModel


class ContentFilters(BaseModel):
    title: str | None = None
    author_id: UUID | None = None
