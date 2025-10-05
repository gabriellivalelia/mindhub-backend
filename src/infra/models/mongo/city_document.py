from uuid import UUID, uuid4

from beanie import Document, Link
from pydantic import Field
from pymongo import IndexModel

from infra.models.mongo.state_document import StateDocument


class CityDocument(Document):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="City name")
    state: Link[StateDocument] = Field(..., description="Reference to state")

    class Settings:
        name = "cities"
        indexes = [
            IndexModel([("name", 1), ("state", 1)], unique=True),
        ]
