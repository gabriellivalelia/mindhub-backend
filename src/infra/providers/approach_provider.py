from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.repos.iapproach_repo import IApproachRepo
from application.use_cases.approach.get_approaches import GetApproachesUseCase


class ApproachProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def GetApproachesUseCase(
        self, approach_repo: IApproachRepo
    ) -> GetApproachesUseCase:
        return GetApproachesUseCase(approach_repo)
