from abc import ABC, abstractmethod

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.city_filters import CityFilters
from domain.city import City
from domain.common.unique_entity_id import UniqueEntityId


class ICityRepo(ABC):
    @abstractmethod
    async def get_by_id(self, id: UniqueEntityId) -> City | None: ...

    @abstractmethod
    async def get(
        self,
        pageable: Pageable,
        filters: CityFilters | None = None,
    ) -> Page[City]: ...
