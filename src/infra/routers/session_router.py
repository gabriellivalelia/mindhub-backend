from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse

from application.services.iauth_service import JWTData
from application.use_cases.session.login import (
    ForbiddenAccessException,
    LoginDTO,
    LoginDTOResponse,
    LoginUseCase,
    UnauthorizedAccessException,
)
from application.use_cases.session.logout import LogoutUseCase, UserNotFoundException

router = APIRouter(route_class=DishkaRoute)
route = "/sessions"


@router.post(
    f"{route}/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginDTOResponse,
    tags=["sessions"],
)
async def login(
    use_case: FromDishka[LoginUseCase],
    dto: Annotated[LoginDTO, Body()],
) -> LoginDTOResponse | JSONResponse:
    try:
        return await use_case.execute(dto)
    except UnauthorizedAccessException as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "message": "Unauthorized",
                "errors": str(exc),
            },
        )
    except ForbiddenAccessException as exc:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "message": "Forbidden",
                "errors": str(exc),
            },
        )


@router.post(
    f"{route}/logout",
    status_code=status.HTTP_200_OK,
    tags=["sessions"],
)
async def logout(
    use_case: FromDishka[LogoutUseCase],
    jwt_data: FromDishka[JWTData],
) -> JSONResponse:
    try:
        await use_case.execute(jwt_data.user.id)
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "User is logged out"}
        )
    except UserNotFoundException as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": str(exc)}
        )
