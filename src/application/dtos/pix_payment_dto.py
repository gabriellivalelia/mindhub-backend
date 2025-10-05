from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, FieldSerializationInfo, field_serializer

from domain.pix_payment import PixPayment


class PixPaymentDTO(BaseModel):
    id: UUID
    amount: float
    provider_payment_id: str
    pix_payload: str
    expires_at: datetime
    status: str

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info: FieldSerializationInfo) -> str:
        return str(id)

    @staticmethod
    def to_dto(entity: PixPayment) -> PixPaymentDTO:
        return PixPaymentDTO(
            id=entity.id.value,
            amount=entity.amount,
            provider_payment_id=entity.provider_payment_id,
            pix_payload=entity.pix_payload,
            expires_at=entity.expires_at,
            status=entity.status.value,
        )
