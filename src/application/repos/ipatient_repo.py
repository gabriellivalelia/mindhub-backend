from abc import ABC, abstractmethod

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.patient_filters import PatientFilters
from domain.common.unique_entity_id import UniqueEntityId
from domain.patient import Patient


class IPatientRepo(ABC):
    @abstractmethod
    async def create(self, entity: Patient) -> Patient: ...

    @abstractmethod
    async def update(self, entity: Patient) -> Patient: ...

    @abstractmethod
    async def get(
        self,
        pageable: Pageable,
        filters: PatientFilters | None = None,
    ) -> Page[Patient]: ...

    @abstractmethod
    async def get_by_id(self, id: UniqueEntityId) -> Patient | None: ...

    @abstractmethod
    async def delete(self, id: UniqueEntityId) -> bool: ...
