from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.psychologist_dto import PsychologistDTO
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.common.unique_entity_id import UniqueEntityId


class RemoveAvailabilitiesDTO(BaseModel):
    availability_datetimes: list[datetime]
    psychologist_id: UUID

    class Config:
        arbitrary_types_allowed = True


class RemoveAvailabilitiesUseCase(IUseCase[RemoveAvailabilitiesDTO, PsychologistDTO]):
    psychologist_repo: IPsychologistRepo

    def __init__(
        self,
        psychologist_repo: IPsychologistRepo,
    ) -> None:
        self.psychologist_repo = psychologist_repo

    async def execute(self, dto: RemoveAvailabilitiesDTO) -> PsychologistDTO:
        availability_datetimes = dto.availability_datetimes

        psychologist = await self.psychologist_repo.get_by_id(UniqueEntityId(dto.psychologist_id))

        if not psychologist:
            raise ApplicationException("Psicólogo não encontrado.")

        if not availability_datetimes:
            raise ApplicationException("É necessário fornecer pelo menos uma disponibilidade para remover.")

        # Remove the availabilities (domain will validate if they exist and are available)
        psychologist.remove_availabilities(availability_datetimes)

        updated_psychologist = await self.psychologist_repo.update(psychologist)
        return PsychologistDTO.to_dto(updated_psychologist)
