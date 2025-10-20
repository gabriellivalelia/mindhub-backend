from abc import ABC, abstractmethod

from domain.city import City
from domain.common.unique_entity_id import UniqueEntityId


class ICityRepo(ABC):
    @abstractmethod
    async def create(self, entity: City) -> City: ...

    @abstractmethod
    async def get_by_id(self, id: UniqueEntityId) -> City | None: ...

    @abstractmethod
    async def get_all_by_state_id(self, state_id: UniqueEntityId) -> list[City]: ...
