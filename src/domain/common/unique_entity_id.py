from typing import Any
from uuid import UUID, uuid4

from domain.common.identifier import Identifier


class UniqueEntityId(Identifier[UUID]):
    def __init__(self, id: UUID | None = None):
        super().__init__(uuid4() if id is None else id)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UniqueEntityId):
            return False

        return str(self.value) == str(other.value)
