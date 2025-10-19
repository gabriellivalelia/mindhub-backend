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
from domain.value_objects.phone_number import PhoneNumber


class UpdatePatientDTO(BaseModel):
    patient_id: UUID
    name: str | None = None
    email: str | None = None
    cpf: str | None = None
    phone_number: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    city_id: UUID | None = None
    profile_picture: UploadFile | None = None
    delete_profile_picture: bool = False

    class Config:
        arbitrary_types_allowed = True


class UpdatePatientUseCase(IUseCase[UpdatePatientDTO, PatientDTO]):
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

    async def execute(self, dto: UpdatePatientDTO) -> PatientDTO:
        found_patient = await self.patient_repo.get_by_id(
            UniqueEntityId(dto.patient_id)
        )
        if not found_patient:
            raise ApplicationException("Patient not found.")

        query_list: list[dict[str, str]] = []

        email = found_patient.email
        if dto.email and dto.email != email.value:
            email = Email(value=dto.email)
            query_list.append({"email": dto.email})

        cpf = found_patient.cpf
        if dto.cpf and dto.cpf != cpf.value:
            cpf = CPF(value=dto.cpf)
            query_list.append({"email": dto.cpf})

        if len(query_list) > 0:
            is_duplicated = await self.user_repo.exists_by(query_list)
            if is_duplicated:
                raise ApplicationException("Duplicated e-mail or cpf.")

        city = found_patient.city
        if dto.city_id:
            city = await self.city_repo.get_by_id(UniqueEntityId(dto.city_id))
            if not city:
                raise ApplicationException("City not found.")

        profile_picture = found_patient.profile_picture
        if dto.delete_profile_picture:
            profile_picture = None
            if found_patient.profile_picture:
                await self.file_service.delete(found_patient.profile_picture.key)

        elif dto.profile_picture:
            # Delete old profile picture and upload new one
            if found_patient.profile_picture:
                await self.file_service.delete(found_patient.profile_picture.key)
            profile_picture = await self.file_service.upload(dto.profile_picture)

        updated_patient = Patient(
            name=dto.name or found_patient.name,
            email=email,
            password=found_patient.password,
            cpf=cpf,
            phone_number=PhoneNumber(value=dto.phone_number)
            if dto.phone_number
            else found_patient.phone_number,
            birth_date=dto.birth_date or found_patient.birth_date,
            gender=GenderEnum(dto.gender) if dto.gender else found_patient.gender,
            city=city,
            profile_picture=profile_picture,
            id=found_patient.id,
        )

        saved_patient = await self.patient_repo.update(updated_patient)
        return PatientDTO.to_dto(saved_patient)
