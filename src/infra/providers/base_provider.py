from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.repos.icity_repo import ICityRepo
from application.repos.ipatient_repo import IPatientRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from application.repos.ispecialty_repo import ISpecialtyRepo
from application.services.iauth_service import IAuthService
from application.services.ifile_service import IFileService
from infra.repos.in_memory.city_repo import InMemoryCityRepo
from infra.repos.in_memory.patient_repo import InMemoryPatientRepo
from infra.repos.in_memory.psychologist_repo import InMemoryPsychologistRepo
from infra.repos.in_memory.specialty_repo import InMemorySpecialtyRepo
from infra.services.bcrypt_auth_service import BcryptAuthService
from infra.services.local_file_service import LocalFileService


class BaseProvider(Provider):
    @provide(scope=Scope.APP)
    def AuthServiceImpl(self) -> IAuthService:
        return BcryptAuthService()

    @provide(scope=Scope.APP)
    def FileServiceImpl(self) -> IFileService:
        return LocalFileService()

    @provide(scope=Scope.REQUEST)
    def PatientRepo(self) -> IPatientRepo:
        return InMemoryPatientRepo()

    @provide(scope=Scope.REQUEST)
    def PscychologistRepo(self) -> IPsychologistRepo:
        return InMemoryPsychologistRepo()

    @provide(scope=Scope.REQUEST)
    def SpecialtyRepo(self) -> ISpecialtyRepo:
        return InMemorySpecialtyRepo()

    @provide(scope=Scope.REQUEST)
    def CityRepo(self) -> ICityRepo:
        return InMemoryCityRepo()
