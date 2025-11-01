from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class UniqueEntityId:
    _value: UUID

    def __init__(self, id: UUID | None = None):
        self._value = uuid4() if id is None else id

    @property
    def value(self):
        return self._value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UniqueEntityId):
            return False

        return str(self.value) == str(other.value)
