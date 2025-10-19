from datetime import datetime
from uuid import UUID

from beanie import Document


class ContentDocument(Document):
    id: UUID
    title: str
    body: str
    author_id: UUID
    created_at: datetime

    class Settings:
        name = "contents"
