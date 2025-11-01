from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.page import Page
from application.common.pageable import Pageable
from application.common.use_case import IUseCase
from application.dtos.appointment_dto import AppointmentDTO
from application.filters.appointment_filters import AppointmentFilters
from application.repos.iappointment_repo import IAppointmentRepo
from domain.common.unique_entity_id import UniqueEntityId


class GetAppointmentByIdDTO(BaseModel):
    appointment_id: UUID


class GetAppointmentByIdUseCase(IUseCase[GetAppointmentByIdDTO, AppointmentDTO]):
    appointment_repo: IAppointmentRepo

    def __init__(self, appointment_repo: IAppointmentRepo) -> None:
        self.appointment_repo = appointment_repo

    async def execute(self, dto: GetAppointmentByIdDTO) -> AppointmentDTO:
        appointment = await self.appointment_repo.get_by_id(UniqueEntityId(dto.appointment_id))

        if not appointment:
            raise ApplicationException("Agendamento não encontrado")

        return AppointmentDTO.to_dto(appointment)


class GetAppointmentsDTO(Pageable, AppointmentFilters): ...


class GetAppointmentsUseCase(IUseCase[GetAppointmentsDTO, Page[AppointmentDTO]]):
    appointment_repo: IAppointmentRepo

    def __init__(self, appointment_repo: IAppointmentRepo) -> None:
        self.appointment_repo = appointment_repo

    async def execute(self, dto: GetAppointmentsDTO) -> Page[AppointmentDTO]:
        pageable = Pageable(page=dto.page, size=dto.size, sort=dto.sort)
        filters = AppointmentFilters(
            start_date=dto.start_date,
            end_date=dto.end_date,
            psychologist_id=dto.psychologist_id,
            patient_id=dto.patient_id,
            status=dto.status,
            availability_id=dto.availability_id,
        )

        page = await self.appointment_repo.get(pageable, filters)
        return Page[AppointmentDTO](
            items=[AppointmentDTO.to_dto(entity) for entity in page.items],
            total=page.total,
            pageable=page.pageable,
        )
