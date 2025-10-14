from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, Query, status

from application.common.page import Page
from application.dtos.approach_dto import ApproachDTO
from application.use_cases.approach.create_approach import (
    CreateApproachDTO,
    CreateApproachUseCase,
)
from application.use_cases.approach.get_approach_by_id import (
    GetApproachByIdDTO,
    GetApproachByIdUseCase,
)
from application.use_cases.approach.get_approaches import (
    GetApproachesDTO,
    GetApproachesUseCase,
)

router = APIRouter(route_class=DishkaRoute)


@router.post(
    "/approaches",
    status_code=status.HTTP_201_CREATED,
    response_model=ApproachDTO,
    tags=["approaches"],
)
async def create_approach(
    dto: CreateApproachDTO,
    use_case: FromDishka[CreateApproachUseCase],
) -> ApproachDTO:
    return await use_case.execute(dto)


@router.get(
    "/approaches/{approach_id}",
    status_code=status.HTTP_200_OK,
    response_model=ApproachDTO,
    tags=["approaches"],
)
async def get_approach_by_id(
    approach_id: Annotated[UUID, Path()],
    use_case: FromDishka[GetApproachByIdUseCase],
) -> ApproachDTO:
    dto = GetApproachByIdDTO(approach_id=approach_id)
    return await use_case.execute(dto)


@router.get(
    "/approaches",
    status_code=status.HTTP_200_OK,
    response_model=Page[ApproachDTO],
    tags=["approaches"],
)
async def get_approaches(
    dto: Annotated[GetApproachesDTO, Query()],
    use_case: FromDishka[GetApproachesUseCase],
) -> Page[ApproachDTO]:
    return await use_case.execute(dto)
