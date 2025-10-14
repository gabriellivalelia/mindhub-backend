from datetime import datetime
from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Path, status
from fastapi.responses import JSONResponse

from application.dtos.appointment_dto import AppointmentDTO
from application.repos.iuser_repo import IUserRepo
from application.services.iauth_service import JWTData
from application.use_cases.appointment.cancel_appointment import (
    CancelAppointmentDTO,
    CancelAppointmentUseCase,
)
from application.use_cases.appointment.reschedule_appointment import (
    RescheduleAppointmentDTO,
    RescheduleAppointmentUseCase,
)
from domain.common.unique_entity_id import UniqueEntityId
from domain.patient import Patient
from domain.psychologist import Psychologist

router = APIRouter(route_class=DishkaRoute)
route = "/appointments"


async def _ensure_user_is_patient_or_psychologist(
    user_repo: IUserRepo, jwt_data: JWTData
) -> None:
    user = await user_repo.get_by_id(UniqueEntityId(jwt_data.id))
    if not user:
        raise Exception("Authenticated user not found")

    # ensure user is Patient or Psychologist
    if not isinstance(user, (Patient, Psychologist)):
        raise Exception(
            "User must be a patient or a psychologist to perform this action"
        )


@router.post(
    f"{route}/{{appointment_id}}/cancel",
    status_code=status.HTTP_200_OK,
    response_model=AppointmentDTO,
    tags=["appointments"],
)
async def cancel_appointment(
    jwt_data: FromDishka[JWTData],
    appointment_id: Annotated[UUID, Path()],
    use_case: FromDishka[CancelAppointmentUseCase],
    user_repo: FromDishka[IUserRepo],
) -> AppointmentDTO | JSONResponse:
    await _ensure_user_is_patient_or_psychologist(user_repo, jwt_data)
    dto = CancelAppointmentDTO(
        appointment_id=appointment_id, requesting_user_id=jwt_data.id
    )
    return await use_case.execute(dto)


@router.post(
    f"{route}/{{appointment_id}}/reschedule",
    status_code=status.HTTP_200_OK,
    response_model=AppointmentDTO,
    tags=["appointments"],
)
async def reschedule_appointment(
    jwt_data: FromDishka[JWTData],
    appointment_id: Annotated[UUID, Path()],
    new_date: Annotated[datetime, Body()],
    use_case: FromDishka[RescheduleAppointmentUseCase],
    user_repo: FromDishka[IUserRepo],
) -> AppointmentDTO | JSONResponse:
    await _ensure_user_is_patient_or_psychologist(user_repo, jwt_data)
    dto = RescheduleAppointmentDTO(
        appointment_id=appointment_id,
        new_date=new_date,
        requesting_user_id=jwt_data.id,
    )
    return await use_case.execute(dto)
