from datetime import date
from typing import Annotated
from uuid import UUID

from application.common.page import Page
from application.dtos.psychologist_dto import PsychologistDTO
from application.use_cases.psychologist.create_psychologist import (
    CreatePsychologistDTO,
    CreatePsychologistUseCase,
)
from application.use_cases.psychologist.get_psychologists import (
    GetPsychologistsDTO,
    GetPsychologistsUseCase,
)
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, File, Form, Query, UploadFile, status
from fastapi.responses import JSONResponse

router = APIRouter(route_class=DishkaRoute)
route = "/psychologists"


@router.post(
    route,
    status_code=status.HTTP_201_CREATED,
    response_model=PsychologistDTO,
    tags=["psychologists"],
)
async def create_psychologist(
    name: Annotated[str, Form(examples=["Gabi"])],
    email: Annotated[str, Form(examples=["gabi@gamil.com"])],
    password: Annotated[str, Form(examples=["AcC123456*"])],
    cpf: Annotated[str, Form(examples=["86231101533"])],
    phone_number: Annotated[str, Form(examples=["71999258225"])],
    birth_date: Annotated[date, Form(examples=["2025-09-16"])],
    gender: Annotated[str, Form(examples=["male"])],
    city_id: Annotated[UUID, Form(examples=["f0678630-c3c0-4d8c-8a2a-1e7555c15cb5"])],
    crp: Annotated[str, Form(examples=["05/5555"])],
    description: Annotated[str, Form(example=["string"])],
    specialty_ids: Annotated[
        list[UUID], Form(examples=[["3fa85f64-5717-4562-b3fc-2c963f66afa6"]])
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


# @router.post(
#     f"{route}/{{psychologist_id}}/availabilities",
#     status_code=status.HTTP_200_OK,
#     response_model=PsychologistDTO,
#     tags=["psychologists"],
# )
# async def add_availabilities(
#     psychologist_id: UUID,
#     request_dto: Annotated[AddAvailabilitiesDTO, Body()],
#     use_case: FromDishka[AddAvailabilitiesUseCase],
#     psychologist_repo: FromDishka[IPsychologistRepo],
# ) -> PsychologistDTO | JSONResponse:
#     dto = AddAvailabilitiesDTO(
#         availability_datetimes=request_dto.availability_datetimes,
#         psychologist_id=request_dto.psychologist_id,
#     )

#     return await use_case.execute(dto)
