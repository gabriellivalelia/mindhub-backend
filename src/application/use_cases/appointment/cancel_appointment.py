from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.appointment_dto import AppointmentDTO
from application.repos.iappointment_repo import IAppointmentRepo
from application.repos.ipatient_repo import IPatientRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.common.unique_entity_id import UniqueEntityId


class CancelAppointmentDTO(BaseModel):
    appointment_id: UUID
    requesting_user_id: UUID


class CancelAppointmentUseCase(IUseCase[CancelAppointmentDTO, AppointmentDTO]):
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

    async def execute(self, dto: CancelAppointmentDTO) -> AppointmentDTO:
        appointment = await self.appointment_repo.get_by_id(
            UniqueEntityId(dto.appointment_id)
        )

        if not appointment:
            raise ApplicationException("Appointment not found.")

        # Authorization: only patient or psychologist related to appointment can cancel
        # authorization: requesting user must be either patient or psychologist on appointment
        if (
            dto.requesting_user_id != appointment.patient_id.value
            and dto.requesting_user_id != appointment.psychologist_id.value
        ):
            raise ApplicationException("Not authorized to cancel this appointment.")

        # perform cancel
        appointment.cancel()

        # if appointment had an availability reserved, unschedule it on psychologist
        if appointment.availability_id:
            psychologist = await self.psychologist_repo.get_by_id(
                appointment.psychologist_id
            )
            if psychologist and psychologist.availabilities:
                # find availability and unschedule
                for av in psychologist.availabilities:
                    if av.id.value == appointment.availability_id.value:
                        av.unschedule()
                        await self.psychologist_repo.update(psychologist)
                        break

        updated = await self.appointment_repo.update(appointment)

        return AppointmentDTO.to_dto(updated)
