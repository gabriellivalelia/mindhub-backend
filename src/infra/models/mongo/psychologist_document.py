from typing import Annotated

from beanie import Indexed, Link
from pydantic import Field

from infra.models.mongo.approach_document import ApproachDocument
from infra.models.mongo.availability_document import AvailabilityDocument
from infra.models.mongo.specialty_document import SpecialtyDocument
from infra.models.mongo.user_document import UserDocument


class PsychologistDocument(UserDocument):
    crp: Annotated[str, Indexed(unique=True)]
    specialties: list[Link[SpecialtyDocument]] = Field(default_factory=list)
    approaches: list[Link[ApproachDocument]] = Field(default_factory=list)
    audiences: list[str] = Field(default_factory=list)
    value_per_appointment: float
    description: str | None = None
    availabilities: list[Link[AvailabilityDocument]] | None = None
