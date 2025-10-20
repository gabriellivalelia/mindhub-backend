from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Path, Query, status

from application.common.page import Page
from application.dtos.city_dto import CityDTO
from application.dtos.state_dto import StateDTO
from application.use_cases.geography.get_cities_by_state_id import (
    GetCitiesByStateIdUseCase,
)
from application.use_cases.geography.get_states import GetStatesDTO, GetStatesUseCase

router = APIRouter(route_class=DishkaRoute)


@router.get(
    "/states",
    status_code=status.HTTP_200_OK,
    response_model=Page[StateDTO],
    tags=["geography"],
)
async def get_states(
    dto: Annotated[GetStatesDTO, Query()],
    use_case: FromDishka[GetStatesUseCase],
) -> Page[StateDTO]:
    return await use_case.execute(dto)


@router.get(
    "/cities/{state_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[CityDTO],
    tags=["geography"],
)
async def get_cities_by_state_id(
    state_id: Annotated[UUID, Path()],
    use_case: FromDishka[GetCitiesByStateIdUseCase],
) -> list[CityDTO]:
    return await use_case.execute(state_id)
