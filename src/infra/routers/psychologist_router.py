from datetime import date, datetime
from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, File, Form, Query, UploadFile, status
from fastapi.responses import JSONResponse

from application.common.page import Page
from application.dtos.psychologist_dto import PsychologistDTO
from application.services.iauth_service import JWTData
from application.use_cases.psychologist.add_availabilities import (
    AddAvailabilitiesDTO,
    AddAvailabilitiesUseCase,
)
from application.use_cases.psychologist.create_psychologist import (
    CreatePsychologistDTO,
    CreatePsychologistUseCase,
)
from application.use_cases.psychologist.get_psychologists import (
    GetPsychologistsDTO,
    GetPsychologistsUseCase,
)

router = APIRouter(route_class=DishkaRoute)
route = "/psychologists"


@router.post(
    route,
    status_code=status.HTTP_201_CREATED,
    response_model=PsychologistDTO,
    tags=["psychologists"],
)
async def create_psychologist(
    name: Annotated[str, Form(examples=["Cleber"])],
    email: Annotated[str, Form(examples=["cleber@psy.com"])],
    password: Annotated[str, Form(examples=["AcC123456*"])],
    cpf: Annotated[str, Form(examples=["86231101533"])],
    phone_number: Annotated[str, Form(examples=["71999258225"])],
    birth_date: Annotated[date, Form(examples=["1999-07-28"])],
    gender: Annotated[str, Form(examples=["male"])],
    city_id: Annotated[UUID, Form(examples=["94b829ad-8c2e-4e96-8d3e-d5ee73784d44"])],
    crp: Annotated[str, Form(examples=["05/5555"])],
    description: Annotated[str, Form(example=["string"])],
    specialty_ids: Annotated[
        list[UUID], Form(examples=[["96c95918-75af-4fa9-b97e-9e72bdd1e4b0"]])
    ],
    approaches: Annotated[list[str], Form(examples=[["tcc"]])],
    audiences: Annotated[list[str], Form(examples=[["children"]])],
    use_case: FromDishka[CreatePsychologistUseCase],
    profile_picture: Annotated[UploadFile | None, File()] = None,
) -> PsychologistDTO | JSONResponse:
    dto = CreatePsychologistDTO(
        name=name,
        email=email,
        password=password,
        cpf=cpf,
        phone_number=phone_number,
        birth_date=birth_date,
        gender=gender,
        city_id=city_id,
        crp=crp,
        description=description,
        specialty_ids=specialty_ids,
        approaches=approaches,
        audiences=audiences,
        profile_picture=profile_picture,
    )
    return await use_case.execute(dto)


@router.get(
    route,
    status_code=status.HTTP_200_OK,
    response_model=Page[PsychologistDTO],
    tags=["psychologists"],
)
async def get_psychologists(
    dto: Annotated[GetPsychologistsDTO, Query()],
    use_case: FromDishka[GetPsychologistsUseCase],
) -> Page[PsychologistDTO]:
    return await use_case.execute(dto)


@router.post(
    f"{route}/availabilities",
    status_code=status.HTTP_200_OK,
    response_model=PsychologistDTO,
    tags=["psychologists"],
)
async def add_availabilities(
    jwt_data: FromDishka[JWTData],
    request_dto: Annotated[
        list[datetime],
        Body(
            examples=[
                [
                    "2025-10-05T18:50:29.022Z",
                    "2025-10-15T18:50:29.022Z",
                    "2025-10-25T18:50:29.022Z",
                ]
            ]
        ),
    ],
    use_case: FromDishka[AddAvailabilitiesUseCase],
) -> PsychologistDTO | JSONResponse:
    dto = AddAvailabilitiesDTO(
        availability_datetimes=request_dto,
        psychologist_id=jwt_data.id,
    )

    return await use_case.execute(dto)
