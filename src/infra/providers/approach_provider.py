from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.repos.iapproach_repo import IApproachRepo
from application.use_cases.approach.create_approach import CreateApproachUseCase
from application.use_cases.approach.get_approach_by_id import GetApproachByIdUseCase
from application.use_cases.approach.get_approaches import GetApproachesUseCase


class ApproachProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def CreateApproachUseCaseInstance(
        self, approach_repo: IApproachRepo
    ) -> CreateApproachUseCase:
        return CreateApproachUseCase(approach_repo)

    @provide(scope=Scope.REQUEST)
    def GetApproachByIdUseCaseInsntance(
        self, approach_repo: IApproachRepo
    ) -> GetApproachByIdUseCase:
        return GetApproachByIdUseCase(approach_repo)

    @provide(scope=Scope.REQUEST)
    def GetApproachesUseCaseInstance(
        self, approach_repo: IApproachRepo
    ) -> GetApproachesUseCase:
        return GetApproachesUseCase(approach_repo)
