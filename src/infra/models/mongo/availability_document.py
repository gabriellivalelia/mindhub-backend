from datetime import datetime
from uuid import UUID

from beanie import Document
from pydantic import Field
from pymongo import IndexModel


class AvailabilityDocument(Document):
    id: UUID
    date: datetime
    available: bool = Field(default=True)

    class Settings:
        name = "availabilities"
        indexes = [
            IndexModel("date"),
            IndexModel("available"),
        ]
