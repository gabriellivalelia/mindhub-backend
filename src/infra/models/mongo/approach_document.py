from uuid import UUID

from beanie import Document
from pymongo import IndexModel


class ApproachDocument(Document):
    id: UUID
    name: str
    description: str

    class Settings:
        name = "approaches"
        indexes = [
            IndexModel("name", unique=True),
        ]
