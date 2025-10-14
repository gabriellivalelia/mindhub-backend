from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from application.services.iauth_service import JWTData
from application.use_cases.user.delete_user import (
    DeleteUserDTO,
    DeleteUserUseCase,
)

router = APIRouter(route_class=DishkaRoute)


@router.delete("/users", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    jwt_data: FromDishka[JWTData],
    use_case: FromDishka[DeleteUserUseCase],
):
    dto = DeleteUserDTO(
        user_id=jwt_data.id,
    )
    await use_case.execute(dto)
    return {"message": "User deleted successfully"}
