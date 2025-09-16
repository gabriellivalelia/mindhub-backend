from uuid import UUID

from pydantic import BaseModel


class CityFilters(BaseModel):
    name: str | None = None
    state_id: UUID | None = None
