# from datetime import datetime
# from uuid import UUID

# from application.common.use_case import IUseCase
# from application.dtos.appointment_dto import AppointmentDTO
# from application.repos.iappointment_repo import IAppointmentRepo
# from domain.appointment import Appointment, AppointmentStatusEnum
# from pydantic import BaseModel


# class CreateAppointmentDTO(BaseModel):
#     date: datetime
#     psychologist_id: UUID
#     pacient_id: UUID
#     avaliability_id: UUID
#     status: AppointmentStatusEnum

#     class Config:
#         arbitrary_types_allowed = True


# class CreateAppointmentUseCase(IUseCase[CreateAppointmentDTO, AppointmentDTO]):
#     appointment_repo: IAppointmentRepo

#     def __init__(
#         self,
#         appointment_repo: IAppointmentRepo,
#     ) -> None:
#         self.appointment_repo = appointment_repo

#     async def execute(self, dto: CreateAppointmentDTO) -> AppointmentDTO:
#         appointment = Appointment(
#             date=dto.date,
#             psychologist_id=dto.psychologist_id,
#             pacient_id=dto.pacient_id,
#             avaliability_id=dto.avaliability_id,
#             status=dto.status,
#         )

#         created_appointment = await self.appointment_repo.save(appointment)
#         return AppointmentDTO.to_dto(created_appointment)
