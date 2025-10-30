from datetime import date, datetime
from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, File, Form, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse

from application.common.page import Page
from application.dtos.appointment_dto import AppointmentDTO
from application.dtos.patient_dto import PatientDTO
from application.services.iauth_service import JWTData
from application.use_cases.patient.create_patient import (
    CreatePatientDTO,
    CreatePatientUseCase,
)

# ...existing code... (delete patient use case removed)
from application.use_cases.patient.get_patient_by_id import (
    GetPatientByIdDTO,
    GetPatientByIdUseCase,
)
from application.use_cases.patient.get_patients import (
    GetPatientsDTO,
    GetPatientsUseCase,
)
from application.use_cases.patient.solicit_schedule_appointment import (
    SolicitScheduleAppointmentDTO,
    SolicitScheduleAppointmentUseCase,
)
from application.use_cases.patient.update_patient import (
    UpdatePatientDTO,
    UpdatePatientUseCase,
)
from infra.routers.utils import ConvertEmptyStrToNoneBeforeValidator

router = APIRouter(route_class=DishkaRoute)
route = "/patients"


@router.post(
    route,
    status_code=status.HTTP_201_CREATED,
    response_model=PatientDTO,
    tags=["patients"],
)
async def create_patient(
    name: Annotated[str, Form(examples=["Gabi"])],
    email: Annotated[str, Form(examples=["gabi@gmail.com"])],
    password: Annotated[str, Form(examples=["AcC123456*"])],
    cpf: Annotated[str, Form(examples=["18071991775"])],
    phone_number: Annotated[str, Form(examples=["71999258225"]), ConvertEmptyStrToNoneBeforeValidator],
    birth_date: Annotated[date, Form(examples=["2025-09-16"])],
    gender: Annotated[str, Form(examples=["male"])],
    city_id: Annotated[
        UUID,
        Form(examples=["c51e05bc-c48b-4229-980e-3841e62ae413"]),
        ConvertEmptyStrToNoneBeforeValidator,
    ],
    use_case: FromDishka[CreatePatientUseCase],
    profile_picture: Annotated[UploadFile | None, File(examples=None), ConvertEmptyStrToNoneBeforeValidator] = None,
) -> PatientDTO | JSONResponse:
    dto = CreatePatientDTO(
        name=name,
        email=email,
        password=password,
        cpf=cpf,
        phone_number=phone_number,
        birth_date=birth_date,
        gender=gender,
        city_id=city_id,
        profile_picture=profile_picture,
    )
    return await use_case.execute(dto)


@router.get(
    f"{route}/{{patient_id}}",
    status_code=status.HTTP_200_OK,
    response_model=PatientDTO,
    tags=["patients"],
)
async def get_patient_by_id(
    patient_id: Annotated[UUID, Path()],
    use_case: FromDishka[GetPatientByIdUseCase],
) -> PatientDTO:
    dto = GetPatientByIdDTO(patient_id=patient_id)
    return await use_case.execute(dto)


@router.get(
    route,
    status_code=status.HTTP_200_OK,
    response_model=Page[PatientDTO],
    tags=["patients"],
)
async def get_patients(
    dto: Annotated[GetPatientsDTO, Query()],
    use_case: FromDishka[GetPatientsUseCase],
) -> Page[PatientDTO]:
    return await use_case.execute(dto)


@router.post(
    f"{route}/solicit-schedule-appointment/" + "{psychologist_id}",
    status_code=status.HTTP_200_OK,
    response_model=AppointmentDTO,
    tags=["patients"],
)
async def solicit_schedule_appointment(
    jwt_data: FromDishka[JWTData],
    appointment_date: Annotated[datetime, Body()],
    psychologist_id: Annotated[UUID, Path()],
    use_case: FromDishka[SolicitScheduleAppointmentUseCase],
) -> AppointmentDTO | JSONResponse:
    dto = SolicitScheduleAppointmentDTO(date=appointment_date, psychologist_id=psychologist_id, patient_id=jwt_data.id)
    return await use_case.execute(dto)


@router.put(
    f"{route}",
    status_code=status.HTTP_200_OK,
    response_model=PatientDTO,
    tags=["patients"],
)
async def update_patient(
    jwt_data: FromDishka[JWTData],
    use_case: FromDishka[UpdatePatientUseCase],
    name: Annotated[str | None, Form(examples=[""])] = None,
    email: Annotated[str | None, Form(examples=[""])] = None,
    cpf: Annotated[str | None, Form(examples=[""])] = None,
    phone_number: Annotated[str | None, Form(examples=[""])] = None,
    birth_date: Annotated[date | None, Form(examples=[""]), ConvertEmptyStrToNoneBeforeValidator] = None,
    gender: Annotated[str | None, Form(examples=[""])] = None,
    city_id: Annotated[UUID | None, Form(examples=[""]), ConvertEmptyStrToNoneBeforeValidator] = None,
    profile_picture: Annotated[UploadFile | None, File(examples=None), ConvertEmptyStrToNoneBeforeValidator] = None,
    delete_profile_picture: Annotated[bool, Form(examples=[False])] = False,
) -> PatientDTO | JSONResponse:
    dto = UpdatePatientDTO(
        patient_id=jwt_data.id,
        name=name,
        email=email,
        cpf=cpf,
        phone_number=phone_number,
        birth_date=birth_date,
        gender=gender,
        city_id=city_id,
        profile_picture=profile_picture,
        delete_profile_picture=delete_profile_picture,
    )
    return await use_case.execute(dto)


# Patient deletion endpoint intentionally removed. User deletion remains at /users/me
