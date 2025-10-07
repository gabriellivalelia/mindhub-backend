from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.repos.icity_repo import ICityRepo
from application.repos.istate_repo import IStateRepo
from application.use_cases.geography.get_cities import GetCitiesUseCase
from application.use_cases.geography.get_states import GetStatesUseCase


class GeographyProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def GetStatesUseCaseInstance(
        self,
        state_repo: IStateRepo,
    ) -> GetStatesUseCase:
        return GetStatesUseCase(state_repo)

    @provide(scope=Scope.REQUEST)
    def GetCitiesUseCaseInstance(
        self,
        city_repo: ICityRepo,
    ) -> GetCitiesUseCase:
        return GetCitiesUseCase(city_repo)
