from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.repos.iuser_repo import IUserRepo
from application.use_cases.user.delete_user import DeleteUserUseCase


class UserProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def DeleteUserUseCaseInstance(
        self,
        user_repo: IUserRepo,
    ) -> DeleteUserUseCase:
        return DeleteUserUseCase(user_repo)
