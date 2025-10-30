from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.appointment_dto import AppointmentDTO
from application.repos.iappointment_repo import IAppointmentRepo
from application.repos.ipatient_repo import IPatientRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from application.services.ipix_payment_service import IPixPaymentService
from domain.appointment import Appointment, AppointmentStatusEnum
from domain.common.unique_entity_id import UniqueEntityId


class SolicitScheduleAppointmentDTO(BaseModel):
    date: datetime
    psychologist_id: UUID
    patient_id: UUID

    class Config:
        arbitrary_types_allowed = True


class SolicitScheduleAppointmentUseCase(IUseCase[SolicitScheduleAppointmentDTO, AppointmentDTO]):
    patient_repo: IPatientRepo
    psychologist_repo: IPsychologistRepo
    appointment_repo: IAppointmentRepo
    pix_payment_service: IPixPaymentService

    def __init__(
        self,
        patient_repo: IPatientRepo,
        psychologist_repo: IPsychologistRepo,
        appointment_repo: IAppointmentRepo,
        pix_payment_service: IPixPaymentService,
    ) -> None:
        self.patient_repo = patient_repo
        self.psychologist_repo = psychologist_repo
        self.appointment_repo = appointment_repo
        self.pix_payment_service = pix_payment_service

    async def execute(self, dto: SolicitScheduleAppointmentDTO) -> AppointmentDTO:
        patient = await self.patient_repo.get_by_id(UniqueEntityId(dto.patient_id))

        if not patient:
            raise ApplicationException("Paciente não encontrado.")

        psychologist = await self.psychologist_repo.get_by_id(UniqueEntityId(dto.psychologist_id))

        if not psychologist:
            raise ApplicationException("Psicólogo não encontrado.")

        # A validação de data passada não é necessária aqui porque:
        # 1. As availabilities do psicólogo já filtram horários passados
        # 2. O método get_availability_by_date vai falhar se o horário não estiver disponível
        # 3. Problemas de timezone entre frontend/backend podem causar falsos positivos

        # Garantir que a data tenha timezone para o banco de dados
        appointment_date = dto.date
        if appointment_date.tzinfo is None:
            appointment_date = appointment_date.replace(tzinfo=timezone.utc)

        availability_id = psychologist.get_availability_by_date(appointment_date)

        pix_payment = await self.pix_payment_service.create_payment(psychologist.value_per_appointment)

        appointment = Appointment(
            date=appointment_date,
            psychologist_id=psychologist.id,
            patient_id=patient.id,
            availability_id=availability_id,
            status=AppointmentStatusEnum.WAITING_FOR_PAYMENT,
            value=psychologist.value_per_appointment,
            pix_payment=pix_payment,
        )

        scheduled_appointment = await self.appointment_repo.create(appointment)
        await self.psychologist_repo.update(psychologist)

        return AppointmentDTO.to_dto(scheduled_appointment)
