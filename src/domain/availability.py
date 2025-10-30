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

        # Validação: não permitir agendar se já passou mais de 1 hora
        # Isso dá margem para diferenças de timezone mas previne agendamentos muito antigos
        now_utc = datetime.now(timezone.utc)
        time_diff_hours = (
            self._normalize_datetime(self.date) - self._normalize_datetime(now_utc)
        ).total_seconds() / 3600

        if time_diff_hours < -1:  # Se passou mais de 1 hora
            raise DomainException("Disponibilidade inválida - horário já passou.")

        self._available = False

    def unschedule(self) -> None:
        if self.available:
            raise DomainException("A disponibilidade já está disponível.")

        # Liberar a disponibilidade (tornar disponível novamente)
        self._available = True

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
