from abc import ABC, abstractmethod

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.specialty_filters import SpecialtyFilters
from domain.common.unique_entity_id import UniqueEntityId
from domain.specialty import Specialty


class ISpecialtyRepo(ABC):
    @abstractmethod
    async def create(self, entity: Specialty) -> Specialty: ...

    @abstractmethod
    async def get_by_id(self, id: UniqueEntityId) -> Specialty | None: ...

    @abstractmethod
    async def get_by_ids(self, ids: list[UniqueEntityId]) -> list[Specialty]: ...

    @abstractmethod
    async def get_all(self) -> list[Specialty]: ...

    @abstractmethod
    async def get(
        self, pageable: Pageable, filters: SpecialtyFilters
    ) -> Page[Specialty]: ...
