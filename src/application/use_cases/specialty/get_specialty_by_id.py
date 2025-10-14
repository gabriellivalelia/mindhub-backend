from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.specialty_dto import SpecialtyDTO
from application.repos.ispecialty_repo import ISpecialtyRepo
from domain.common.unique_entity_id import UniqueEntityId


class GetSpecialtyByIdDTO(BaseModel):
    specialty_id: UUID


class GetSpecialtyByIdUseCase(IUseCase[GetSpecialtyByIdDTO, SpecialtyDTO]):
    specialty_repo: ISpecialtyRepo

    def __init__(self, specialty_repo: ISpecialtyRepo) -> None:
        self.specialty_repo = specialty_repo

    async def execute(self, dto: GetSpecialtyByIdDTO) -> SpecialtyDTO:
        specialty = await self.specialty_repo.get_by_id(
            UniqueEntityId(dto.specialty_id)
        )

        if not specialty:
            raise ApplicationException("Specialty not found.")

        return SpecialtyDTO.to_dto(specialty)
