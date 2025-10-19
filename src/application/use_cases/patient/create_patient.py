from datetime import date
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.patient_dto import PatientDTO
from application.repos.icity_repo import ICityRepo
from application.repos.ipatient_repo import IPatientRepo
from application.repos.iuser_repo import IUserRepo
from application.services.iauth_service import IAuthService
from application.services.ifile_service import IFileService
from domain.common.unique_entity_id import UniqueEntityId
from domain.patient import Patient
from domain.user import GenderEnum
from domain.value_objects.cpf import CPF
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from domain.value_objects.phone_number import PhoneNumber


class CreatePatientDTO(BaseModel):
    name: str
    email: str
    password: str
    cpf: str
    phone_number: str
    birth_date: date
    gender: str
    city_id: UUID
    profile_picture: UploadFile | None = None

    class Config:
        arbitrary_types_allowed = True


class CreatePatientUseCase(IUseCase[CreatePatientDTO, PatientDTO]):
    user_repo: IUserRepo
    patient_repo: IPatientRepo
    city_repo: ICityRepo
    file_service: IFileService
    auth_service: IAuthService

    def __init__(
        self,
        user_repo: IUserRepo,
        patient_repo: IPatientRepo,
        city_repo: ICityRepo,
        file_service: IFileService,
        auth_service: IAuthService,
    ) -> None:
        self.user_repo = user_repo
        self.patient_repo = patient_repo
        self.city_repo = city_repo
        self.file_service = file_service
        self.auth_service = auth_service

    async def execute(self, dto: CreatePatientDTO) -> PatientDTO:
        email = Email(value=dto.email)
        cpf = CPF(value=dto.cpf)

        is_duplicated = await self.user_repo.exists_by(
            [{"email": email.value}, {"cpf": cpf.value}]
        )
        if is_duplicated:
            raise ApplicationException("Duplicated e-mail or cpf.")

        city = await self.city_repo.get_by_id(UniqueEntityId(dto.city_id))
        if not city:
            raise ApplicationException("City not found.")

        password = Password(value=dto.password)
        hashed_password = await self.auth_service.hash_password(password)
        profile_picture = (
            await self.file_service.upload(dto.profile_picture)
            if dto.profile_picture is not None
            else None
        )

        phone_number = PhoneNumber(value=dto.phone_number)
        patient = Patient(
            name=dto.name,
            email=email,
            password=hashed_password,
            cpf=cpf,
            phone_number=phone_number,
            birth_date=dto.birth_date,
            gender=GenderEnum(dto.gender),
            city=city,
            profile_picture=profile_picture,
        )

        created_patient = await self.patient_repo.create(patient)
        return PatientDTO.to_dto(created_patient)
