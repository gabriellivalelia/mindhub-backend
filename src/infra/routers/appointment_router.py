from datetime import datetime
from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Path, Query, status
from fastapi.responses import JSONResponse

from application.common.page import Page
from application.dtos.appointment_dto import AppointmentDTO
from application.services.iauth_service import JWTData
from application.use_cases.appointment.cancel_appointment import (
    CancelAppointmentDTO,
    CancelAppointmentUseCase,
)
from application.use_cases.appointment.get_appointment import (
    GetAppointmentByIdDTO,
    GetAppointmentByIdUseCase,
    GetAppointmentsDTO,
    GetAppointmentsUseCase,
)
from application.use_cases.appointment.reschedule_appointment import (
    RescheduleAppointmentDTO,
    RescheduleAppointmentUseCase,
)

router = APIRouter(route_class=DishkaRoute)
route = "/appointments"


@router.patch(
    f"{route}/{{appointment_id}}/cancel",
    status_code=status.HTTP_200_OK,
    response_model=AppointmentDTO,
    tags=["appointments"],
)
async def cancel_appointment(
    jwt_data: FromDishka[JWTData],
    appointment_id: Annotated[UUID, Path()],
    use_case: FromDishka[CancelAppointmentUseCase],
) -> AppointmentDTO | JSONResponse:
    dto = CancelAppointmentDTO(
        appointment_id=appointment_id, requesting_user_id=jwt_data.id
    )
    return await use_case.execute(dto)


@router.patch(
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
) -> AppointmentDTO | JSONResponse:
    dto = RescheduleAppointmentDTO(
        appointment_id=appointment_id,
        new_date=new_date,
        requesting_user_id=jwt_data.id,
    )
    return await use_case.execute(dto)


@router.get(
    f"{route}/{{appointment_id}}",
    status_code=status.HTTP_200_OK,
    response_model=AppointmentDTO,
    tags=["appointments"],
)
async def get_appointment_by_id(
    appointment_id: Annotated[UUID, Path()],
    use_case: FromDishka[GetAppointmentByIdUseCase],
) -> AppointmentDTO:
    dto = GetAppointmentByIdDTO(appointment_id=appointment_id)
    return await use_case.execute(dto)


@router.get(
    route,
    status_code=status.HTTP_200_OK,
    response_model=Page[AppointmentDTO],
    tags=["appointments"],
)
async def get_appointments(
    dto: Annotated[GetAppointmentsDTO, Query()],
    use_case: FromDishka[GetAppointmentsUseCase],
) -> Page[AppointmentDTO]:
    return await use_case.execute(dto)
