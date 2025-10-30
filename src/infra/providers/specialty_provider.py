from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.repos.ispecialty_repo import ISpecialtyRepo
from application.use_cases.specialty.create_specialty import CreateSpecialtyUseCase
from application.use_cases.specialty.get_specialties import GetSpecialtiesUseCase
from application.use_cases.specialty.get_specialty_by_id import GetSpecialtyByIdUseCase


class SpecialtyProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def CreateSpecialtyUseCaseInstance(self, specialty_repo: ISpecialtyRepo) -> CreateSpecialtyUseCase:
        return CreateSpecialtyUseCase(specialty_repo)

    @provide(scope=Scope.REQUEST)
    def GetSpecialtiesUseCaseInstance(self, specialty_repo: ISpecialtyRepo) -> GetSpecialtiesUseCase:
        return GetSpecialtiesUseCase(specialty_repo)

    @provide(scope=Scope.REQUEST)
    def GetSpecialtyByIdUseCase(self, specialty_repo: ISpecialtyRepo) -> GetSpecialtyByIdUseCase:
        return GetSpecialtyByIdUseCase(specialty_repo)
