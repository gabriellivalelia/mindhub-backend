from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, Query, status

from application.common.page import Page
from application.dtos.specialty_dto import SpecialtyDTO
from application.use_cases.specialty.create_specialty import (
    CreateSpecialtyDTO,
    CreateSpecialtyUseCase,
)
from application.use_cases.specialty.get_specialties import (
    GetSpecialtiesDTO,
    GetSpecialtiesUseCase,
)
from application.use_cases.specialty.get_specialty_by_id import (
    GetSpecialtyByIdDTO,
    GetSpecialtyByIdUseCase,
)

router = APIRouter(route_class=DishkaRoute)


@router.post(
    "/specialties",
    status_code=status.HTTP_201_CREATED,
    response_model=SpecialtyDTO,
    tags=["specialties"],
)
async def create_specialty(
    dto: CreateSpecialtyDTO,
    use_case: FromDishka[CreateSpecialtyUseCase],
) -> SpecialtyDTO:
    return await use_case.execute(dto)


@router.get(
    "/specialties/{specialty_id}",
    status_code=status.HTTP_200_OK,
    response_model=SpecialtyDTO,
    tags=["specialties"],
)
async def get_specialty_by_id(
    specialty_id: Annotated[UUID, Path()],
    use_case: FromDishka[GetSpecialtyByIdUseCase],
) -> SpecialtyDTO:
    dto = GetSpecialtyByIdDTO(specialty_id=specialty_id)
    return await use_case.execute(dto)


@router.get(
    "/specialties",
    status_code=status.HTTP_200_OK,
    response_model=Page[SpecialtyDTO],
    tags=["specialties"],
)
async def get_specialties(
    dto: Annotated[GetSpecialtiesDTO, Query()],
    use_case: FromDishka[GetSpecialtiesUseCase],
) -> Page[SpecialtyDTO]:
    return await use_case.execute(dto)
