from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Path, Query, status

from application.common.page import Page
from application.dtos.content_dto import ContentDTO
from application.services.iauth_service import JWTData
from application.use_cases.content.create_content import (
    CreateContentDTO,
    CreateContentUseCase,
)
from application.use_cases.content.delete_content import (
    DeleteContentDTO,
    DeleteContentUseCase,
)
from application.use_cases.content.get_content_by_id import (
    GetContentByIdDTO,
    GetContentByIdUseCase,
)
from application.use_cases.content.get_contents import (
    GetContentsDTO,
    GetContentsUseCase,
)
from application.use_cases.content.update_content import (
    UpdateContentDTO,
    UpdateContentUseCase,
)

router = APIRouter(route_class=DishkaRoute)


@router.post(
    "/contents",
    status_code=status.HTTP_201_CREATED,
    response_model=ContentDTO,
    tags=["contents"],
)
async def create_content(
    jwt_data: FromDishka[JWTData],
    title: Annotated[str, Body()],
    body: Annotated[str, Body()],
    use_case: FromDishka[CreateContentUseCase],
) -> ContentDTO:
    dto = CreateContentDTO(
        title=title,
        body=body,
        author_id=jwt_data.id,
    )
    return await use_case.execute(dto)


@router.get(
    "/contents/{content_id}",
    status_code=status.HTTP_200_OK,
    response_model=ContentDTO,
    tags=["contents"],
)
async def get_content_by_id(
    content_id: Annotated[UUID, Path()],
    use_case: FromDishka[GetContentByIdUseCase],
) -> ContentDTO:
    dto = GetContentByIdDTO(content_id=content_id)
    return await use_case.execute(dto)


@router.get(
    "/contents",
    status_code=status.HTTP_200_OK,
    response_model=Page[ContentDTO],
    tags=["contents"],
)
async def get_contents(
    dto: Annotated[GetContentsDTO, Query()],
    use_case: FromDishka[GetContentsUseCase],
) -> Page[ContentDTO]:
    return await use_case.execute(dto)


@router.put(
    "/contents/{content_id}",
    status_code=status.HTTP_200_OK,
    response_model=ContentDTO,
    tags=["contents"],
)
async def update_content(
    jwt_data: FromDishka[JWTData],
    content_id: Annotated[UUID, Path()],
    title: Annotated[str, Body()],
    body: Annotated[str, Body()],
    use_case: FromDishka[UpdateContentUseCase],
) -> ContentDTO:
    dto = UpdateContentDTO(
        content_id=content_id,
        title=title,
        body=body,
        requesting_user_id=jwt_data.id,
    )
    return await use_case.execute(dto)


@router.delete(
    "/contents/{content_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["contents"],
)
async def delete_content(
    jwt_data: FromDishka[JWTData],
    content_id: Annotated[UUID, Path()],
    use_case: FromDishka[DeleteContentUseCase],
):
    dto = DeleteContentDTO(
        content_id=content_id,
        requesting_user_id=jwt_data.id,
    )
    await use_case.execute(dto)
