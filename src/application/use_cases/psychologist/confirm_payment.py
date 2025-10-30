from uuid import UUID

from pydantic import BaseModel

from application.common.use_case import IUseCase
from application.dtos.appointment_dto import AppointmentDTO
from application.repos.iappointment_repo import IAppointmentRepo
from domain.common.exception import DomainException
from domain.common.unique_entity_id import UniqueEntityId


class ConfirmPaymentDTO(BaseModel):
    appointment_id: UUID
    psychologist_id: UUID


class ConfirmPaymentUseCase(IUseCase[ConfirmPaymentDTO, AppointmentDTO]):
    appointment_repository: IAppointmentRepo

    def __init__(
        self,
        appointment_repository: IAppointmentRepo,
    ) -> None:
        self.appointment_repository = appointment_repository

    async def execute(self, dto: ConfirmPaymentDTO) -> AppointmentDTO:
        # Buscar o agendamento
        appointment = await self.appointment_repository.get_by_id(UniqueEntityId(dto.appointment_id))

        if not appointment:
            raise DomainException("Agendamento não encontrado")

        # Verificar se o psicólogo é o dono da consulta
        if appointment.psychologist_id.value != dto.psychologist_id:
            raise DomainException("Você não tem permissão para modificar este agendamento")

        # Confirmar o agendamento
        appointment.confirm()

        # Salvar
        updated_appointment = await self.appointment_repository.update(appointment)

        return AppointmentDTO.to_dto(updated_appointment)
