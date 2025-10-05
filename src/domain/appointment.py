from datetime import datetime
from enum import Enum

from domain.common.entity import Entity
from domain.common.exception import DomainException
from domain.common.guard import Guard
from domain.common.unique_entity_id import UniqueEntityId
from domain.pix_payment import PixPayment

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
        patient_id: UniqueEntityId,
        psychologist_id: UniqueEntityId,
        value: float,
        pix_payment: PixPayment,
        duration_min: int = DEFAULT_DURATION_MIN,
        status: AppointmentStatusEnum = AppointmentStatusEnum.SCHEDULED,
        availability_id: UniqueEntityId | None = None,
        id: UniqueEntityId | None = None,
    ) -> None:
        Guard.against_undefined_bulk(
            [
                {"argument": date, "argument_name": "date"},
                {"argument": patient_id, "argument_name": "patient_id"},
                {"argument": psychologist_id, "argument_name": "psychologist_id"},
                {"argument": value, "argument_name": "value"},
                {"argument": pix_payment, "argument_name": "pix_payment"},
                {"argument": duration_min, "argument_name": "duration_min"},
                {"argument": status, "argument_name": "status"},
            ]
        )
        if duration_min <= 0:
            raise DomainException("Duration must be positive")

        super().__init__(id)

        self._date = date
        self._patient_id = patient_id
        self._psychologist_id = psychologist_id
        self._value = value
        self._pix_payment = pix_payment
        self._duration_min = duration_min
        self._status = status
        self._availability_id = availability_id

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def patient_id(self) -> UniqueEntityId:
        return self._patient_id

    @property
    def psychologist_id(self) -> UniqueEntityId:
        return self._psychologist_id

    @property
    def value(self) -> float:
        return self._value

    @property
    def pix_payment(self) -> PixPayment:
        return self._pix_payment

    @property
    def duration_min(self) -> int:
        return self._duration_min

    @property
    def availability_id(self) -> UniqueEntityId | None:
        return self._availability_id

    @property
    def status(self) -> AppointmentStatusEnum:
        return self._status

    def confirm(self) -> None:
        """Confirm the appointment"""
        self._status = AppointmentStatusEnum.CONFIRMED

    def cancel(self) -> None:
        """Cancel the appointment"""
        self._status = AppointmentStatusEnum.CANCELED

    def complete(self) -> None:
        """Mark the appointment as completed"""
        self._status = AppointmentStatusEnum.COMPLETED
