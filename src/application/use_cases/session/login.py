from pydantic import BaseModel, Field

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.repos.iuser_repo import IUserRepo
from application.services.iauth_service import IAuthService
from domain.value_objects.password import Password


class UnauthorizedAccessException(ApplicationException):
    def __init__(self, message: str):
        super().__init__(message)


class ForbiddenAccessException(ApplicationException):
    def __init__(self, message: str):
        super().__init__(message)


class LoginDTO(BaseModel):
    email: str = Field(examples=["gabi@gamil.com"])
    password: str = Field(examples=["AcC123456*"])


class LoginDTOResponse(BaseModel):
    access_token: str
    refresh_token: str


class LoginUseCase(IUseCase[LoginDTO, LoginDTOResponse]):
    user_repo: IUserRepo
    auth_service: IAuthService

    def __init__(self, user_repo: IUserRepo, auth_service: IAuthService) -> None:
        self.user_repo = user_repo
        self.auth_service = auth_service

    async def execute(self, dto: LoginDTO) -> LoginDTOResponse:
        found_user = await self.user_repo.get_by_email(email=dto.email)
        if found_user is None:
            raise UnauthorizedAccessException("Wrong e-mail or password")

        is_match = await self.auth_service.verify_password(
            Password(value=dto.password), found_user.password
        )
        if not is_match:
            raise UnauthorizedAccessException("Wrong e-mail or password")
        access_token, refresh_token = self.auth_service.sign_jwt_tokens(found_user)
        user_id = str(found_user.id.value)
        await self.auth_service.save_authenticated_user(user_id, refresh_token)

        return LoginDTOResponse(access_token=access_token, refresh_token=refresh_token)
