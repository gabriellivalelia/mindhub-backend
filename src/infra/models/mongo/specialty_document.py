from uuid import UUID

from beanie import Document
from pymongo import IndexModel


class SpecialtyDocument(Document):
    id: UUID
    name: str
    description: str

    class Settings:
        name = "specialties"
        indexes = [
            IndexModel("name", unique=True),
        ]
