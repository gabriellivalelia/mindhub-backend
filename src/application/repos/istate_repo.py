from abc import ABC, abstractmethod

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.state_filters import StateFilters
from domain.common.unique_entity_id import UniqueEntityId
from domain.state import State


class IStateRepo(ABC):
    @abstractmethod
    async def get_by_id(self, id: UniqueEntityId) -> State | None: ...

    @abstractmethod
    async def get(
        self,
        pageable: Pageable,
        filters: StateFilters | None = None,
    ) -> Page[State]: ...
