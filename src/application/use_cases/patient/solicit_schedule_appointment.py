from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.appointment_dto import AppointmentDTO
from application.repos.iappointment_repo import IAppointmentRepo
from application.repos.ipatient_repo import IPatientRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.appointment import Appointment, AppointmentStatusEnum
from domain.common.unique_entity_id import UniqueEntityId
from domain.pix_payment import PixPayment


class SolicitScheduleAppointmentDTO(BaseModel):
    date: datetime
    psychologist_id: UUID
    patient_id: UUID

    class Config:
        arbitrary_types_allowed = True


class ScheduleAppointmentUseCase(
    IUseCase[SolicitScheduleAppointmentDTO, AppointmentDTO]
):
    patient_repo: IPatientRepo
    psychologist_repo: IPsychologistRepo
    appointment_repo: IAppointmentRepo

    def __init__(
        self,
        patient_repo: IPatientRepo,
        psychologist_repo: IPsychologistRepo,
        appointment_repo: IAppointmentRepo,
    ) -> None:
        self.patient_repo = patient_repo
        self.psychologist_repo = psychologist_repo
        self.appointment_repo = appointment_repo

    async def execute(self, dto: SolicitScheduleAppointmentDTO) -> AppointmentDTO:
        patient = await self.patient_repo.get_by_id(UniqueEntityId(dto.patient_id))

        if not patient:
            raise ApplicationException("Patient not found.")

        psychologist = await self.psychologist_repo.get_by_id(
            UniqueEntityId(dto.psychologist_id)
        )

        if not psychologist:
            raise ApplicationException("Psychologist not found.")

        availability_id = psychologist.get_availability_by_date(dto.date)

        appointment = Appointment(
            date=dto.date,
            psychologist_id=psychologist.id,
            patient_id=patient.id,
            availability_id=availability_id,
            status=AppointmentStatusEnum.SCHEDULED,
            value=psychologist.value_per_appointment,
            pix_payment=PixPayment(
                psychologist.value_per_appointment, "to do", "to do", datetime.now()
            ),
        )

        scheduled_appointment = await self.appointment_repo.create(appointment)
        await self.psychologist_repo.update(psychologist)

        return AppointmentDTO.to_dto(scheduled_appointment)
