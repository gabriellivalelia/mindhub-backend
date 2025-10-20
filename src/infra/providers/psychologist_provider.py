from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.repos.iapproach_repo import IApproachRepo
from application.repos.icity_repo import ICityRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from application.repos.ispecialty_repo import ISpecialtyRepo
from application.repos.iuser_repo import IUserRepo
from application.services.iauth_service import IAuthService
from application.services.ifile_service import IFileService
from application.use_cases.psychologist.add_availabilities import (
    AddAvailabilitiesUseCase,
)
from application.use_cases.psychologist.create_psychologist import (
    CreatePsychologistUseCase,
)
from application.use_cases.psychologist.get_psychologist_by_id import (
    GetPsychologistByIdUseCase,
)
from application.use_cases.psychologist.get_psychologists import (
    GetPsychologistsUseCase,
)
from application.use_cases.psychologist.remove_availabilities import (
    RemoveAvailabilitiesUseCase,
)
from application.use_cases.psychologist.update_psychologist import (
    UpdatePsychologistUseCase,
)


class PsychologistProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def CreatePsychologistUseCaseInstance(
        self,
        user_repo: IUserRepo,
        psychologist_repo: IPsychologistRepo,
        specialty_repo: ISpecialtyRepo,
        approach_repo: IApproachRepo,
        city_repo: ICityRepo,
        file_service: IFileService,
        auth_service: IAuthService,
    ) -> CreatePsychologistUseCase:
        return CreatePsychologistUseCase(
            user_repo=user_repo,
            psychologist_repo=psychologist_repo,
            specialty_repo=specialty_repo,
            approach_repo=approach_repo,
            city_repo=city_repo,
            file_service=file_service,
            auth_service=auth_service,
        )

    @provide(scope=Scope.REQUEST)
    def GetPsychologistsUseCaseInstance(
        self,
        psychologist_repo: IPsychologistRepo,
    ) -> GetPsychologistsUseCase:
        return GetPsychologistsUseCase(psychologist_repo)

    @provide(scope=Scope.REQUEST)
    def AddAvailabilitiesUseCaseInstance(
        self, psychologist_repo: IPsychologistRepo
    ) -> AddAvailabilitiesUseCase:
        return AddAvailabilitiesUseCase(psychologist_repo)

    @provide(scope=Scope.REQUEST)
    def RemoveAvailabilitiesUseCaseInstance(
        self, psychologist_repo: IPsychologistRepo
    ) -> RemoveAvailabilitiesUseCase:
        return RemoveAvailabilitiesUseCase(psychologist_repo)

    @provide(scope=Scope.REQUEST)
    def UpdatePsychologistUseCaseInstance(
        self,
        user_repo: IUserRepo,
        psychologist_repo: IPsychologistRepo,
        city_repo: ICityRepo,
        specialty_repo: ISpecialtyRepo,
        approach_repo: IApproachRepo,
        file_service: IFileService,
        auth_service: IAuthService,
    ) -> UpdatePsychologistUseCase:
        return UpdatePsychologistUseCase(
            user_repo=user_repo,
            psychologist_repo=psychologist_repo,
            city_repo=city_repo,
            specialty_repo=specialty_repo,
            approach_repo=approach_repo,
            file_service=file_service,
            auth_service=auth_service,
        )

    @provide(scope=Scope.REQUEST)
    def GetPsychologistByIdUseCaseInstance(
        self,
        psychologist_repo: IPsychologistRepo,
    ) -> GetPsychologistByIdUseCase:
        return GetPsychologistByIdUseCase(psychologist_repo)
