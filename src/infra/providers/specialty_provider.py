from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.repos.ispecialty_repo import ISpecialtyRepo
from application.use_cases.specialty.get_specialties import GetSpecialtiesUseCase


class SpecialtyProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def GetSpecialtiesUseCase(
        self, specialty_repo: ISpecialtyRepo
    ) -> GetSpecialtiesUseCase:
        return GetSpecialtiesUseCase(specialty_repo)
