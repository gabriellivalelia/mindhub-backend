from datetime import datetime

from domain.appointment import Appointment
from domain.common.entity import Entity
from domain.common.exception import DomainException
from domain.common.guard import Guard
from domain.common.unique_entity_id import UniqueEntityId


class Availability(Entity):
    def __init__(
        self,
        date: datetime,
        appointment_id: UniqueEntityId | None = None,
        available: bool = True,
        id: UniqueEntityId | None = None,
    ) -> None:
        Guard.against_undefined(date, "date")

        super().__init__(id)

        self._date = date
        self._appointment_id = appointment_id
        self._available = available

    def schedule(self, appointment: Appointment):
        if self.available:
            raise DomainException("Appointment is already fullfield.")

        Guard.against_undefined(appointment, "appointment")

        self._available = True
        self._appointment_id = appointment.id

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def appointment_id(self) -> UniqueEntityId | None:
        return self._appointment_id

    @property
    def available(self) -> bool:
        return self._available
