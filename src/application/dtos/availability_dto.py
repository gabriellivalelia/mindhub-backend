from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, FieldSerializationInfo, field_serializer

from domain.availability import Availability


class AvailabilityDTO(BaseModel):
    id: UUID
    date: datetime
    available: bool

    @field_serializer("id")
    def serialize_id(self, value: UUID | None, _info: FieldSerializationInfo) -> str | None:
        return str(value) if value else None

    @staticmethod
    def to_dto(entity: Availability) -> AvailabilityDTO:
        return AvailabilityDTO(
            id=entity.id.value,
            date=entity.date,
            available=entity.available,
        )
