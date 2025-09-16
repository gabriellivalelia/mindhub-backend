from abc import ABC, abstractmethod

from domain.common.unique_entity_id import UniqueEntityId
from domain.specialty import Specialty


class ISpecialtyRepo(ABC):
    @abstractmethod
    async def get_by_ids(self, ids: list[UniqueEntityId]) -> list[Specialty]: ...
