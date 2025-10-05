from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, FieldSerializationInfo, field_serializer

from application.dtos.pix_payment_dto import PixPaymentDTO
from domain.appointment import Appointment


class AppointmentDTO(BaseModel):
    id: UUID
    date: datetime
    patient_id: UUID
    psychologist_id: UUID
    pix_payment: PixPaymentDTO
    duration_min: int
    status: str
    availability_id: UUID | None = None

    @field_serializer("id", "appointment_id")
    def serialize_id(
        self, value: UUID | None, _info: FieldSerializationInfo
    ) -> str | None:
        return str(value) if value else None

    @staticmethod
    def to_dto(entity: Appointment) -> AppointmentDTO:
        return AppointmentDTO(
            id=entity.id.value,
            date=entity.date,
            patient_id=entity.patient_id.value,
            psychologist_id=entity.psychologist_id.value,
            pix_payment=PixPaymentDTO.to_dto(entity.pix_payment),
            duration_min=entity.duration_min,
            status=entity.status.value,
            availability_id=entity.availability_id.value
            if entity.availability_id
            else None,
        )
