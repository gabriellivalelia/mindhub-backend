from uuid import UUID

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.repos.iuser_repo import IUserRepo
from application.services.iauth_service import IAuthService
from domain.common.unique_entity_id import UniqueEntityId


class UserNotFoundException(ApplicationException):
    def __init__(self):
        super().__init__("User not found")


class LogoutUseCase(IUseCase[UUID, None]):
    user_repo: IUserRepo
    auth_service: IAuthService

    def __init__(self, user_repo: IUserRepo, auth_service: IAuthService) -> None:
        self.user_repo = user_repo
        self.auth_service = auth_service

    async def execute(self, dto: UUID) -> None:
        found_user = await self.user_repo.get_by_id(UniqueEntityId(dto))
        if found_user is None:
            raise UserNotFoundException()

        await self.auth_service.de_authenticate_user(str(dto))
