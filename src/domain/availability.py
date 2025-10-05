from datetime import datetime

from domain.common.entity import Entity
from domain.common.exception import DomainException
from domain.common.guard import Guard
from domain.common.unique_entity_id import UniqueEntityId


class Availability(Entity):
    def __init__(
        self,
        date: datetime,
        available: bool = True,
        id: UniqueEntityId | None = None,
    ) -> None:
        Guard.against_undefined(date, "date")

        super().__init__(id)

        self._date = date
        self._available = available

    def schedule(self):
        if not self.available:
            raise DomainException("Appointment is already scheduled.")

        self._available = False

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def available(self) -> bool:
        return self._available
