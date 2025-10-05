from uuid import UUID

from beanie import Document
from pydantic import Field
from pymongo import IndexModel


class StateDocument(Document):
    id: UUID
    name: str
    abbreviation: str = Field(..., max_length=2)

    class Settings:
        name = "states"
        indexes = [
            IndexModel("abbreviation", unique=True),
        ]
