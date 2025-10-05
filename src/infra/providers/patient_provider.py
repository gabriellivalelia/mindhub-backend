from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.repos.icity_repo import ICityRepo
from application.repos.ipatient_repo import IPatientRepo
from application.repos.iuser_repo import IUserRepo
from application.services.iauth_service import IAuthService
from application.services.ifile_service import IFileService
from application.use_cases.patient.create_patient import (
    CreatePatientUseCase,
)
from application.use_cases.patient.get_patients import GetPatientsUseCase


class PatientProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def CreatePatientUseCaseInstance(
        self,
        user_repo: IUserRepo,
        patient_repo: IPatientRepo,
        city_repo: ICityRepo,
        file_service: IFileService,
        auth_service: IAuthService,
    ) -> CreatePatientUseCase:
        return CreatePatientUseCase(
            user_repo=user_repo,
            patient_repo=patient_repo,
            city_repo=city_repo,
            file_service=file_service,
            auth_service=auth_service,
        )

    @provide(scope=Scope.REQUEST)
    def GetPatientsUseCaseInstance(
        self,
        patient_repo: IPatientRepo,
    ) -> GetPatientsUseCase:
        return GetPatientsUseCase(patient_repo)
