from __future__ import annotations

from abc import ABC

from domain.common.unique_entity_id import UniqueEntityId


class Entity(ABC):
    _id: UniqueEntityId

    def __init__(self, id: UniqueEntityId | None) -> None:
        self._id = id if id is not None else UniqueEntityId()

    def equals(self, obj: Entity):
        if obj is None or not isinstance(obj, Entity):
            return False

        return self.id == obj.id

    @property
    def id(self) -> UniqueEntityId:
        return self._id
