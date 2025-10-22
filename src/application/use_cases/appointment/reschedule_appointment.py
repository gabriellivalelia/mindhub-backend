from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.appointment_dto import AppointmentDTO
from application.repos.iappointment_repo import IAppointmentRepo
from application.repos.ipatient_repo import IPatientRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.common.unique_entity_id import UniqueEntityId


class RescheduleAppointmentDTO(BaseModel):
    appointment_id: UUID
    new_date: datetime
    requesting_user_id: UUID


class RescheduleAppointmentUseCase(IUseCase[RescheduleAppointmentDTO, AppointmentDTO]):
    appointment_repo: IAppointmentRepo
    psychologist_repo: IPsychologistRepo
    patient_repo: IPatientRepo

    def __init__(
        self,
        appointment_repo: IAppointmentRepo,
        psychologist_repo: IPsychologistRepo,
        patient_repo: IPatientRepo,
    ) -> None:
        self.appointment_repo = appointment_repo
        self.psychologist_repo = psychologist_repo
        self.patient_repo = patient_repo

    async def execute(self, dto: RescheduleAppointmentDTO) -> AppointmentDTO:
        appointment = await self.appointment_repo.get_by_id(
            UniqueEntityId(dto.appointment_id)
        )

        if not appointment:
            raise ApplicationException("Appointment not found.")

        # Authorization: only patient or psychologist related to appointment can reschedule
        req_id = str(dto.requesting_user_id)
        if req_id != str(appointment.patient_id.value) and req_id != str(
            appointment.psychologist_id.value
        ):
            raise ApplicationException("Not authorized to reschedule this appointment.")

        # Use timezone-aware comparison (new_date may include tzinfo)
        now = datetime.now(timezone.utc)
        # If dto.new_date is naive, assume UTC for comparison by converting
        new_date = dto.new_date
        if new_date.tzinfo is None:
            # attach UTC tzinfo to naive datetimes to compare safely
            new_date = new_date.replace(tzinfo=timezone.utc)

        if new_date < now:
            raise ApplicationException("Cannot reschedule to a past date.")

        # attempt to schedule new availability in psychologist and free old availability
        psychologist = await self.psychologist_repo.get_by_id(
            appointment.psychologist_id
        )
        if not psychologist:
            raise ApplicationException("Psychologist not found.")

        # schedule new availability (this will raise if not available)
        new_availability_id = psychologist.get_availability_by_date(dto.new_date)

        # free old availability if present
        if appointment.availability_id:
            for av in psychologist.availabilities or []:
                if av.id.value == appointment.availability_id.value:
                    av.unschedule()
                    break

        # use domain method to reschedule
        appointment.reschedule(dto.new_date, new_availability_id)

        # persist psychologist changes and appointment
        await self.psychologist_repo.update(psychologist)
        updated = await self.appointment_repo.update(appointment)

        return AppointmentDTO.to_dto(updated)
