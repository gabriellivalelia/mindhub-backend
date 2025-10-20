from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.repos.iappointment_repo import IAppointmentRepo
from application.repos.icity_repo import ICityRepo
from application.repos.ipatient_repo import IPatientRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from application.repos.iuser_repo import IUserRepo
from application.services.iauth_service import IAuthService
from application.services.ifile_service import IFileService
from application.services.ipix_payment_service import IPixPaymentService
from application.use_cases.approach.appointment.cancel_appointment import (
    CancelAppointmentUseCase,
)
from application.use_cases.approach.appointment.get_appointment import (
    GetAppointmentByIdUseCase,
    GetAppointmentsUseCase,
)
from application.use_cases.approach.appointment.reschedule_appointment import (
    RescheduleAppointmentUseCase,
)
from application.use_cases.patient.create_patient import (
    CreatePatientUseCase,
)
from application.use_cases.patient.delete_patient import DeletePatientUseCase
from application.use_cases.patient.get_patient_by_id import GetPatientByIdUseCase
from application.use_cases.patient.get_patients import GetPatientsUseCase
from application.use_cases.patient.solicit_schedule_appointment import (
    SolicitScheduleAppointmentUseCase,
)
from application.use_cases.patient.update_patient import UpdatePatientUseCase


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

    @provide(scope=Scope.REQUEST)
    def UpdatePatientUseCaseInstance(
        self,
        user_repo: IUserRepo,
        patient_repo: IPatientRepo,
        city_repo: ICityRepo,
        file_service: IFileService,
        auth_service: IAuthService,
    ) -> UpdatePatientUseCase:
        return UpdatePatientUseCase(
            user_repo=user_repo,
            patient_repo=patient_repo,
            city_repo=city_repo,
            file_service=file_service,
            auth_service=auth_service,
        )

    @provide(scope=Scope.REQUEST)
    def SoliciteScheduleAppointmentUseCaseInstance(
        self,
        patient_repo: IPatientRepo,
        psychologist_repo: IPsychologistRepo,
        appointment_repo: IAppointmentRepo,
        pix_payment_service: IPixPaymentService,
    ) -> SolicitScheduleAppointmentUseCase:
        return SolicitScheduleAppointmentUseCase(
            patient_repo, psychologist_repo, appointment_repo, pix_payment_service
        )

    @provide(scope=Scope.REQUEST)
    def DeletePatientUseCaseInstance(
        self,
        patient_repo: IPatientRepo,
    ) -> DeletePatientUseCase:
        return DeletePatientUseCase(patient_repo)

    @provide(scope=Scope.REQUEST)
    def GetPatientByIdUseCaseInstance(
        self,
        patient_repo: IPatientRepo,
    ) -> GetPatientByIdUseCase:
        return GetPatientByIdUseCase(patient_repo)

    @provide(scope=Scope.REQUEST)
    def CancelAppointmentUseCaseInstance(
        self,
        appointment_repo: IAppointmentRepo,
        psychologist_repo: IPsychologistRepo,
        patient_repo: IPatientRepo,
    ) -> CancelAppointmentUseCase:
        return CancelAppointmentUseCase(
            appointment_repo=appointment_repo,
            psychologist_repo=psychologist_repo,
            patient_repo=patient_repo,
        )

    @provide(scope=Scope.REQUEST)
    def RescheduleAppointmentUseCaseInstance(
        self,
        appointment_repo: IAppointmentRepo,
        psychologist_repo: IPsychologistRepo,
        patient_repo: IPatientRepo,
    ) -> RescheduleAppointmentUseCase:
        return RescheduleAppointmentUseCase(
            appointment_repo=appointment_repo,
            psychologist_repo=psychologist_repo,
            patient_repo=patient_repo,
        )

    @provide(scope=Scope.REQUEST)
    def GetAppointmentsUseCaseInstance(
        self, appointment_repo: IAppointmentRepo
    ) -> GetAppointmentsUseCase:
        return GetAppointmentsUseCase(appointment_repo)

    @provide(scope=Scope.REQUEST)
    def GetAppointmentByIdUseCaseInstance(
        self, appointment_repo: IAppointmentRepo
    ) -> GetAppointmentByIdUseCase:
        return GetAppointmentByIdUseCase(appointment_repo)
