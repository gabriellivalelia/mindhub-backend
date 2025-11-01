from datetime import date
from uuid import UUID

from fastapi import UploadFile
from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.psychologist_dto import PsychologistDTO
from application.repos.iapproach_repo import IApproachRepo
from application.repos.icity_repo import ICityRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from application.repos.ispecialty_repo import ISpecialtyRepo
from application.repos.iuser_repo import IUserRepo
from application.services.iauth_service import IAuthService
from application.services.ifile_service import IFileService
from domain.common.unique_entity_id import UniqueEntityId
from domain.psychologist import AudienceEnum, Psychologist
from domain.user import GenderEnum
from domain.value_objects.cpf import CPF
from domain.value_objects.crp import CRP
from domain.value_objects.email import Email
from domain.value_objects.phone_number import PhoneNumber


class UpdatePsychologistDTO(BaseModel):
    psychologist_id: UUID
    name: str | None = None
    email: str | None = None
    cpf: str | None = None
    phone_number: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    city_id: UUID | None = None
    crp: str | None = None
    description: str | None = None
    specialty_ids: list[UUID] | None = None
    approach_ids: list[UUID] | None = None
    audiences: list[str] | None = None
    value_per_appointment: float | None = None
    profile_picture: UploadFile | None = None
    delete_profile_picture: bool = False

    class Config:
        arbitrary_types_allowed = True


class UpdatePsychologistUseCase(IUseCase[UpdatePsychologistDTO, PsychologistDTO]):
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
        city_repo: ICityRepo,
        specialty_repo: ISpecialtyRepo,
        approach_repo: IApproachRepo,
        file_service: IFileService,
        auth_service: IAuthService,
    ) -> None:
        self.user_repo = user_repo
        self.psychologist_repo = psychologist_repo
        self.city_repo = city_repo
        self.specialty_repo = specialty_repo
        self.approach_repo = approach_repo
        self.file_service = file_service
        self.auth_service = auth_service

    async def execute(self, dto: UpdatePsychologistDTO) -> PsychologistDTO:
        found_psychologist = await self.psychologist_repo.get_by_id(UniqueEntityId(dto.psychologist_id))
        if not found_psychologist:
            raise ApplicationException("Psicólogo não encontrado.")

        query_list: list[dict[str, str]] = []

        email = found_psychologist.email
        if dto.email and dto.email != email.value:
            email = Email(value=dto.email)
            query_list.append({"email": dto.email})

        cpf = found_psychologist.cpf
        if dto.cpf and dto.cpf != cpf.value:
            cpf = CPF(value=dto.cpf)
            query_list.append({"email": dto.cpf})

        crp = found_psychologist.crp
        if dto.crp and dto.crp != crp.value:
            crp = CRP(value=dto.crp)
            query_list.append({"crp": dto.crp})

        if len(query_list) > 0:
            is_duplicated = await self.user_repo.exists_by(query_list)
            if is_duplicated:
                raise ApplicationException("E-mail, CPF ou CRP duplicado.")

        specialties = found_psychologist.specialties
        if dto.specialty_ids:
            specialties = await self.specialty_repo.get_by_ids([UniqueEntityId(id) for id in dto.specialty_ids])
            if len(specialties) != len(dto.specialty_ids):
                raise ApplicationException("Uma ou mais especialidades não foram encontradas.")

        approaches = found_psychologist.approaches
        if dto.approach_ids:
            approaches = await self.approach_repo.get_by_ids([UniqueEntityId(id) for id in dto.approach_ids])
            if len(approaches) != len(dto.approach_ids):
                raise ApplicationException("Uma ou mais abordagens não foram encontradas.")

        city = found_psychologist.city
        if dto.city_id:
            city = await self.city_repo.get_by_id(UniqueEntityId(dto.city_id))
            if not city:
                raise ApplicationException("Cidade não encontrada.")

        profile_picture = found_psychologist.profile_picture
        if dto.delete_profile_picture:
            profile_picture = None
            if found_psychologist.profile_picture:
                await self.file_service.delete(found_psychologist.profile_picture.key)

        elif dto.profile_picture:
            # Delete old profile picture and upload new one
            if found_psychologist.profile_picture:
                await self.file_service.delete(found_psychologist.profile_picture.key)
            profile_picture = await self.file_service.upload(dto.profile_picture)

        updated_psychologist = Psychologist(
            name=dto.name or found_psychologist.name,
            email=email,
            password=found_psychologist.password,
            cpf=cpf,
            phone_number=PhoneNumber(value=dto.phone_number) if dto.phone_number else found_psychologist.phone_number,
            birth_date=dto.birth_date or found_psychologist.birth_date,
            gender=GenderEnum(dto.gender) if dto.gender else found_psychologist.gender,
            city=city,
            crp=crp,
            description=dto.description or found_psychologist.description,
            specialties=specialties,
            approaches=approaches,
            audiences=[AudienceEnum(audience) for audience in dto.audiences]
            if dto.audiences
            else found_psychologist.audiences,
            value_per_appointment=dto.value_per_appointment
            if dto.value_per_appointment is not None
            else found_psychologist.value_per_appointment,
            availabilities=found_psychologist.availabilities,
            profile_picture=profile_picture,
            id=found_psychologist.id,
        )

        saved_psychologist = await self.psychologist_repo.update(updated_psychologist)
        return PsychologistDTO.to_dto(saved_psychologist)
