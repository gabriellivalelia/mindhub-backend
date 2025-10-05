from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AppointmentFilters(BaseModel):
    date: datetime | None = None
    psychologist_id: UUID | None = None
    patient_id: UUID | None = None
    status: str | None = None
    availability_id: UUID | None = None
    appointment_id: UUID | None = None
