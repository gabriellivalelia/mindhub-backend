from datetime import datetime, timezone

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

        # Normalizar data removendo microsegundos para consistência
        if date.tzinfo is None:
            self._date = date.replace(tzinfo=timezone.utc, microsecond=0)
        else:
            self._date = date.astimezone(timezone.utc).replace(microsecond=0)
        self._available = available

    def schedule(self):
        if not self.available:
            raise DomainException("A consulta já está agendada.")

        if self._normalize_datetime(self.date) < self._normalize_datetime(
            datetime.now()
        ):
            raise DomainException("Disponibilidade inválida.")

        self._available = False

    def unschedule(self) -> None:
        if self.available:
            raise DomainException("A disponibilidade já está disponível.")

        self._available = False

    def is_date_equals_to(self, i_date: datetime):
        return self._normalize_datetime(i_date) == self._normalize_datetime(self.date)

    def _normalize_datetime(self, dt: datetime) -> datetime:
        # Normalizar para UTC e remover microsegundos para comparação
        if dt.tzinfo is None:
            normalized = dt.replace(tzinfo=timezone.utc, microsecond=0)
        else:
            normalized = dt.astimezone(timezone.utc).replace(microsecond=0)
        return normalized

    @property
    def normalized_date(self) -> datetime:
        return self._normalize_datetime(self._date)

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def available(self) -> bool:
        return self._available
