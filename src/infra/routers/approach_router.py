from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from application.common.page import Page
from application.dtos.approach_dto import ApproachDTO
from application.use_cases.approach.get_approaches import (
    GetApproachesDTO,
    GetApproachesUseCase,
)

router = APIRouter(route_class=DishkaRoute)


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
