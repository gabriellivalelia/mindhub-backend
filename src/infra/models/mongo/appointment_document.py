from datetime import datetime
from uuid import UUID

from beanie import Document, Link
from pydantic import Field

from domain.appointment import AppointmentStatusEnum


class PixPaymentDocument(Document):
    id: UUID
    amount: float
    provider_payment_id: str
    pix_payload: str
    expires_at: datetime
    status: str

    class Settings:
        name = "pix_payments"


class AppointmentDocument(Document):
    id: UUID
    date: datetime
    patient_id: UUID
    psychologist_id: UUID
    value: float
    pix_payment: Link[PixPaymentDocument]
    duration_min: int = Field(default=50)
    status: str = Field(default=AppointmentStatusEnum.WAITING_FOR_PAYMENT.value)
    availability_id: UUID | None = None

    class Settings:
        name = "appointments"
