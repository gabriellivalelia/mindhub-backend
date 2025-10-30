from datetime import date
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.availability_dto import AvailabilityDTO
from application.dtos.psychologist_dto import PsychologistDTO
from application.repos.iapproach_repo import IApproachRepo
from application.repos.icity_repo import ICityRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from application.repos.ispecialty_repo import ISpecialtyRepo
from application.repos.iuser_repo import IUserRepo
from application.services.iauth_service import IAuthService
from application.services.ifile_service import IFileService
from domain.common.exception import DomainException
from domain.common.unique_entity_id import UniqueEntityId
from domain.psychologist import AudienceEnum, Psychologist
from domain.user import GenderEnum
from domain.value_objects.cpf import CPF
from domain.value_objects.crp import CRP
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from domain.value_objects.phone_number import PhoneNumber


class CreatePsychologistDTO(BaseModel):
    name: str
    email: str
    password: str
    cpf: str
    phone_number: str
    birth_date: date
    gender: str
    city_id: UUID
    crp: str
    specialty_ids: list[UUID]
    approach_ids: list[UUID]
    audiences: list[str]
    value_per_appointment: float
    description: str | None = None
    availabilities: list[AvailabilityDTO] | None = None
    profile_picture: UploadFile | None = None

    class Config:
        arbitrary_types_allowed = True


class CreatePsychologistUseCase(IUseCase[CreatePsychologistDTO, PsychologistDTO]):
    user_repo: IUserRepo
    psychologist_repo: IPsychologistRepo
    city_repo: ICityRepo
    specialty_repo: ISpecialtyRepo
    approach_repo: IApproachRepo
    file_service: IFileService
    auth_service: IAuthService

    def __init__(
        self,
        user_repo: IUserRepo,
        psychologist_repo: IPsychologistRepo,
        specialty_repo: ISpecialtyRepo,
        approach_repo: IApproachRepo,
        city_repo: ICityRepo,
        file_service: IFileService,
        auth_service: IAuthService,
    ) -> None:
        self.user_repo = user_repo
        self.psychologist_repo = psychologist_repo
        self.specialty_repo = specialty_repo
        self.approach_repo = approach_repo
        self.city_repo = city_repo
        self.file_service = file_service
        self.auth_service = auth_service

    async def execute(self, dto: CreatePsychologistDTO) -> PsychologistDTO:
        email = Email(value=dto.email)
        cpf = CPF(value=dto.cpf)
        crp = CRP(value=dto.crp)

        is_duplicated = await self.user_repo.exists_by([{"email": email.value}, {"cpf": cpf.value}, {"crp": crp.value}])
        if is_duplicated:
            raise ApplicationException("Duplicated e-mail, cpf or crp.")

        city = await self.city_repo.get_by_id(UniqueEntityId(dto.city_id))
        if not city:
            raise DomainException("City not found.")

        specialties = await self.specialty_repo.get_by_ids([UniqueEntityId(id) for id in dto.specialty_ids])
        if len(specialties) != len(dto.specialty_ids):
            raise DomainException("One or more specialties were not found.")

        approaches = await self.approach_repo.get_by_ids([UniqueEntityId(id) for id in dto.approach_ids])
        if len(approaches) != len(dto.approach_ids):
            raise DomainException("One or more approaches were not found.")

        audiences = [AudienceEnum(audience) for audience in dto.audiences]

        password = Password(value=dto.password)
        hashed_password = await self.auth_service.hash_password(password)
        profile_picture = (
            await self.file_service.upload(dto.profile_picture) if dto.profile_picture is not None else None
        )

        phone_number = PhoneNumber(value=dto.phone_number)
        psychologist = Psychologist(
            name=dto.name,
            email=email,
            password=hashed_password,
            cpf=cpf,
            phone_number=phone_number,
            birth_date=dto.birth_date,
            gender=GenderEnum(dto.gender),
            city=city,
            crp=crp,
            description=dto.description,
            specialties=specialties,
            approaches=approaches,
            audiences=audiences,
            value_per_appointment=dto.value_per_appointment,
            profile_picture=profile_picture,
        )
        created_psychologist = await self.psychologist_repo.create(psychologist)
        return PsychologistDTO.to_dto(created_psychologist)
