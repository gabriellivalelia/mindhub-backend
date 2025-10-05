from abc import ABC, abstractmethod

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.appointment_filters import AppointmentFilters
from domain.appointment import Appointment
from domain.common.unique_entity_id import UniqueEntityId


class IAppointmentRepo(ABC):
    @abstractmethod
    async def create(self, entity: Appointment) -> Appointment: ...

    @abstractmethod
    async def get(
        self,
        pageable: Pageable,
        filters: AppointmentFilters | None = None,
    ) -> Page[Appointment]: ...

    @abstractmethod
    async def get_by_id(self, id: UniqueEntityId) -> Appointment | None: ...
