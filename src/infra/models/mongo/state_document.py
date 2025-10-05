from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field
from pymongo import IndexModel


class StateDocument(Document):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="State name")
    abbreviation: str = Field(..., description="State abbreviation", max_length=2)

    class Settings:
        name = "states"
        indexes = [
            IndexModel("abbreviation", unique=True),
        ]
