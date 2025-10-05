from abc import ABC, abstractmethod

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.psychologist_filters import PsychologistFilters
from domain.common.unique_entity_id import UniqueEntityId
from domain.psychologist import Psychologist


class IPsychologistRepo(ABC):
    @abstractmethod
    async def create(self, entity: Psychologist) -> Psychologist: ...

    @abstractmethod
    async def update(self, entity: Psychologist) -> Psychologist: ...

    @abstractmethod
    async def get(
        self,
        pageable: Pageable,
        filters: PsychologistFilters | None = None,
    ) -> Page[Psychologist]: ...

    @abstractmethod
    async def get_by_id(self, id: UniqueEntityId) -> Psychologist | None: ...
