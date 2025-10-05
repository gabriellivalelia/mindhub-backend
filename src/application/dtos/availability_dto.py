from __future__ import annotations

from datetime import datetime
from uuid import UUID

from domain.availability import Availability
from pydantic import BaseModel, FieldSerializationInfo, field_serializer


class AvailabilityDTO(BaseModel):
    id: UUID
    date: datetime
    available: bool
    appointment_id: UUID | None = None

    @field_serializer("id", "appointment_id")
    def serialize_id(
        self, value: UUID | None, _info: FieldSerializationInfo
    ) -> str | None:
        return str(value) if value else None

    @staticmethod
    def to_dto(entity: Availability) -> AvailabilityDTO:
        return AvailabilityDTO(
            id=entity.id.value,
            date=entity.date,
            available=entity.available,
            appointment_id=entity.appointment_id.value
            if entity.appointment_id
            else None,
        )
