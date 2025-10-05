from abc import ABC, abstractmethod

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.availability_filters import AvailabilityFilters
from domain.availability import Availability
from domain.common.unique_entity_id import UniqueEntityId


class IAvailabilityRepo(ABC):
    @abstractmethod
    async def create(self, entity: Availability) -> Availability: ...

    @abstractmethod
    async def get(
        self,
        pageable: Pageable,
        filters: AvailabilityFilters | None = None,
    ) -> Page[Availability]: ...

    @abstractmethod
    async def get_by_id(self, id: UniqueEntityId) -> Availability | None: ...
