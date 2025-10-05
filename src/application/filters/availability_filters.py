from datetime import datetime

from pydantic import BaseModel


class AvailabilityFilters(BaseModel):
    date: datetime | None = None
    available: bool | None = None
