from uuid import UUID

from beanie import Document, Link
from pymongo import IndexModel

from infra.models.mongo.state_document import StateDocument


class CityDocument(Document):
    id: UUID
    name: str
    state: Link[StateDocument]

    class Settings:
        name = "cities"
        indexes = [
            IndexModel([("name", 1), ("state", 1)], unique=True),
        ]
