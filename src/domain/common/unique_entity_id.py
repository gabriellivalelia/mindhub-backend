from uuid import UUID, uuid7

from domain.common.identifier import Identifier


class UniqueEntityId(Identifier[UUID]):
    def __init__(self, id: UUID | None = None):
        super().__init__(uuid7() if id is None else id)
