from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.psychologist_dto import PsychologistDTO
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.common.unique_entity_id import UniqueEntityId


class GetPsychologistByIdDTO(BaseModel):
    psychologist_id: UUID


class GetPsychologistByIdUseCase(IUseCase[GetPsychologistByIdDTO, PsychologistDTO]):
    psychologist_repo: IPsychologistRepo

    def __init__(self, psychologist_repo: IPsychologistRepo) -> None:
        self.psychologist_repo = psychologist_repo

    async def execute(self, dto: GetPsychologistByIdDTO) -> PsychologistDTO:
        psychologist = await self.psychologist_repo.get_by_id(
            UniqueEntityId(dto.psychologist_id)
        )

        if not psychologist:
            raise ApplicationException("Psychologist not found.")

        return PsychologistDTO.to_dto(psychologist)
