from abc import ABC, abstractmethod

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.content_filters import ContentFilters
from domain.common.unique_entity_id import UniqueEntityId
from domain.content import Content


class IContentRepo(ABC):
    @abstractmethod
    async def create(self, entity: Content) -> Content: ...

    @abstractmethod
    async def get(
        self, pageable: Pageable, filters: ContentFilters | None = None
    ) -> Page[Content]: ...

    @abstractmethod
    async def get_by_id(self, id: UniqueEntityId) -> Content | None: ...

    @abstractmethod
    async def update(self, entity: Content) -> Content: ...

    @abstractmethod
    async def delete(self, id: UniqueEntityId) -> bool: ...
