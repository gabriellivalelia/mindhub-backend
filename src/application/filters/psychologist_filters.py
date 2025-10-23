from uuid import UUID

from pydantic import BaseModel

from domain.psychologist import AudienceEnum
from domain.user import GenderEnum


class PsychologistFilters(BaseModel):
    name: str | None = None
    gender: GenderEnum | None = None
    specialty_ids: set[UUID] | None = None
    approach_ids: set[UUID] | None = None
    audiences: set[AudienceEnum] | None = None
    max_price: float | None = None

    class Config:
        extra = "forbid"
