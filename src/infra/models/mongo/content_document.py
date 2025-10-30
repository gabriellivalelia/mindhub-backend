from datetime import datetime
from uuid import UUID

from beanie import Document, Link

from infra.models.mongo.psychologist_document import PsychologistDocument


class ContentDocument(Document):
    id: UUID
    title: str
    body: str
    author_id: UUID
    author: Link[PsychologistDocument] | None = None
    created_at: datetime

    class Settings:
        name = "contents"
