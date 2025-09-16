from datetime import datetime
from enum import Enum

from domain.common.entity import Entity
from domain.common.exception import DomainException
from domain.common.guard import Guard
from domain.common.unique_entity_id import UniqueEntityId
from domain.patient import Patient
from domain.pix_payment import PixPayment
from domain.psychologist import Psychologist

# TODO

DEFAULT_DURATION_MIN = 50


class AppointmentStatusEnum(Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    COMPLETED = "completed"


class Appointment(Entity):
    def __init__(
        self,
        date: datetime,
        patient: Patient,
        psychologist: Psychologist,
        pix_payment: PixPayment,
        duration_min: int = DEFAULT_DURATION_MIN,
        status: AppointmentStatusEnum = AppointmentStatusEnum.SCHEDULED,
        id: UniqueEntityId | None = None,
    ) -> None:
        Guard.against_undefined_bulk(
            [
                {"argument": date, "argument_name": "date"},
                {"argument": patient, "argument_name": "patient"},
                {"argument": psychologist, "argument_name": "psychologist"},
                {"argument": pix_payment, "argument_name": "pix_payment"},
                {"argument": duration_min, "argument_name": "duration_min"},
                {"argument": status, "argument_name": "status"},
            ]
        )
        if duration_min <= 0:
            raise DomainException("Duration must be positive")

        super().__init__(id)

        self._date = date
        self._patient = patient
        self._psychologist = psychologist
        self._pix_payment = pix_payment
        self._duration_min = duration_min
        self._status = status

    def confirm(self) -> None:
        """Confirm the appointment"""
        self._status = AppointmentStatusEnum.CONFIRMED

    def cancel(self) -> None:
        """Cancel the appointment"""
        self._status = AppointmentStatusEnum.CANCELED

    def complete(self) -> None:
        """Mark the appointment as completed"""
        self._status = AppointmentStatusEnum.COMPLETED
