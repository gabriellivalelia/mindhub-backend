from datetime import datetime
from uuid import UUID

from application.common.use_case import IUseCase
from application.dtos.appointment_dto import AppointmentDTO
from application.repos.iappointment_repo import IAppointmentRepo
from application.repos.iavailability_repo import IAvailabilityRepo
from application.repos.ipatient_repo import IPatientRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.appointment import Appointment, AppointmentStatusEnum
from domain.common.exception import DomainException
from domain.patient import Patient
from pydantic import BaseModel


class ScheduleAppointmentDTO(BaseModel):
    date: datetime
    psychologist_id: UUID
    entity: Patient

    class Config:
        arbitrary_types_allowed = True


class ScheduleAppointmentUseCase(IUseCase[ScheduleAppointmentDTO, AppointmentDTO]):
    patient_repo: IPatientRepo
    psychologist_repo: IPsychologistRepo
    availability_repo: IAvailabilityRepo
    appointment_repo: IAppointmentRepo

    def __init__(
        self,
        patient_repo: IPatientRepo,
        psychologist_repo: IPsychologistRepo,
        availability_repo: IAvailabilityRepo,
        appointment_repo: IAppointmentRepo,
    ) -> None:
        self.patient_repo = patient_repo
        self.psychologist_repo = psychologist_repo
        self.availability_repo = availability_repo
        self.appointment_repo = appointment_repo

    async def execute(self, dto: ScheduleAppointmentDTO) -> AppointmentDTO:
        date = dto.date
        psychologist_id = dto.psychologist_id
        entity = dto.entity

        if not date:
            raise DomainException("No appotintment date provided.")

        if not psychologist_id:
            raise DomainException("No psychologist id provided.")

        psychologist = await self.psychologist_repo.get_by_id(psychologist_id)
        if not psychologist:
            raise DomainException("Psychologist not found.")

        if not psychologist.availabilities:
            raise DomainException("Psychologist has no availabilities.")

        psychologist_avalabilities = psychologist.availabilities

        availability = psychologist_avalabilities.filter(date=date)

        if not availability:
            raise DomainException("No availability found for the given date.")

        if not availability.available:
            raise DomainException("The selected date is not available.")

        appoitment = Appointment(
            date=date,
            psychologist_id=psychologist_id,
            patient_id=entity.id,
            availability_id=availability.id,
            status=AppointmentStatusEnum.SCHEDULED,
            value=150.0,
            pix_payment=None,
        )

        scheduled_appointment = await self.appointment_repo.save(appoitment)
        await self.availability_repo.schedule(availability.id, appoitment.id)

        return AppointmentDTO.to_dto(scheduled_appointment)
