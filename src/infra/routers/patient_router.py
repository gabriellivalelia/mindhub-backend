from datetime import date
from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, File, Form, Query, UploadFile, status
from fastapi.responses import JSONResponse

from application.common.page import Page
from application.dtos.patient_dto import PatientDTO
from application.use_cases.patient.create_patient import (
    CreatePatientDTO,
    CreatePatientUseCase,
)
from application.use_cases.patient.get_patients import (
    GetPatientsDTO,
    GetPatientsUseCase,
)

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
    email: Annotated[str, Form(examples=["gabi@gamil.com"])],
    password: Annotated[str, Form(examples=["AcC123456*"])],
    cpf: Annotated[str, Form(examples=["86231101533"])],
    phone_number: Annotated[str, Form(examples=["71999258225"])],
    birth_date: Annotated[date, Form(examples=["2025-09-16"])],
    gender: Annotated[str, Form(examples=["male"])],
    city_id: Annotated[UUID, Form(examples=["f0678630-c3c0-4d8c-8a2a-1e7555c15cb5"])],
    use_case: FromDishka[CreatePatientUseCase],
    profile_picture: Annotated[UploadFile | None, File(examples=None)] = None,
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
