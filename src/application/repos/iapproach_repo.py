from abc import ABC, abstractmethod

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.approach_filters import ApproachFilters
from domain.approach import Approach
from domain.common.unique_entity_id import UniqueEntityId


class IApproachRepo(ABC):
    @abstractmethod
    async def create(self, entity: Approach) -> Approach: ...

    @abstractmethod
    async def get_by_id(self, id: UniqueEntityId) -> Approach | None: ...

    @abstractmethod
    async def get_by_ids(self, ids: list[UniqueEntityId]) -> list[Approach]: ...

    @abstractmethod
    async def get(
        self,
        pageable: Pageable,
        filters: ApproachFilters | None = None,
    ) -> Page[Approach]: ...
