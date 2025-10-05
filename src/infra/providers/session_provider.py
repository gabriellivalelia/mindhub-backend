from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.repos.iuser_repo import IUserRepo
from application.services.iauth_service import IAuthService
from application.use_cases.session.login import LoginUseCase
from application.use_cases.session.logout import LogoutUseCase


class SessionProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def LoginUseCaseInstance(
        self, user_repo: IUserRepo, auth_service: IAuthService
    ) -> LoginUseCase:
        return LoginUseCase(user_repo, auth_service)

    @provide(scope=Scope.REQUEST)
    def LogoutUseCaseInstance(
        self, user_repo: IUserRepo, auth_service: IAuthService
    ) -> LogoutUseCase:
        return LogoutUseCase(user_repo, auth_service)
