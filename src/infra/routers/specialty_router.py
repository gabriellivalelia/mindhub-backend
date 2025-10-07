from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from application.common.page import Page
from application.dtos.specialty_dto import SpecialtyDTO
from application.use_cases.specialty.get_specialties import (
    GetSpecialtiesDTO,
    GetSpecialtiesUseCase,
)

router = APIRouter(route_class=DishkaRoute)


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
