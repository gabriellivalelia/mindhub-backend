from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer

from application.repos.iuser_repo import IUserRepo
from application.services.iauth_service import IAuthService, JWTData
from application.use_cases.session.login import LoginUseCase
from application.use_cases.session.logout import LogoutUseCase
from application.use_cases.session.me import MeUseCase


class SessionProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def LoginUseCaseInstance(self, user_repo: IUserRepo, auth_service: IAuthService) -> LoginUseCase:
        return LoginUseCase(user_repo, auth_service)

    @provide(scope=Scope.REQUEST)
    def LogoutUseCaseInstance(self, user_repo: IUserRepo, auth_service: IAuthService) -> LogoutUseCase:
        return LogoutUseCase(user_repo, auth_service)

    @provide(scope=Scope.REQUEST)
    def MeUseCaseInstance(self, user_repo: IUserRepo) -> MeUseCase:
        return MeUseCase(user_repo)

    @provide(scope=Scope.REQUEST)
    async def AuthMiddleware(self, request: Request, auth_service: IAuthService) -> JWTData:
        credentials = await HTTPBearer(auto_error=True)(request)
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Autenticação falhou",
            )

        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Esquema de autenticação inválido",
            )

        decoded = await auth_service.decode_access_token(credentials.credentials)
        if decoded is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token inválido ou expirado",
            )

        tokens = await auth_service.get_tokens(str(decoded.id))
        if len(tokens) == 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token de autenticação não encontrado. Usuário provavelmente não está logado. Por favor, faça login novamente",
            )

        return decoded
