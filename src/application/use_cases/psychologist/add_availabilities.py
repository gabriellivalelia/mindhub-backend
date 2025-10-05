from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.psychologist_dto import PsychologistDTO
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.availability import Availability
from domain.common.unique_entity_id import UniqueEntityId


class AddAvailabilitiesDTO(BaseModel):
    availability_datetimes: list[datetime]
    psychologist_id: UUID

    class Config:
        arbitrary_types_allowed = True


class AddAvailabilitiesUseCase(IUseCase[AddAvailabilitiesDTO, PsychologistDTO]):
    psychologist_repo: IPsychologistRepo

    def __init__(
        self,
        psychologist_repo: IPsychologistRepo,
    ) -> None:
        self.psychologist_repo = psychologist_repo

    async def execute(self, dto: AddAvailabilitiesDTO) -> PsychologistDTO:
        availability_datetimes = dto.availability_datetimes

        psychologist = await self.psychologist_repo.get_by_id(
            UniqueEntityId(dto.psychologist_id)
        )

        if not psychologist:
            raise ApplicationException("Psychologist not found.")

        availabiliies: list[Availability] = []
        for availability_datetime in availability_datetimes:
            availability = Availability(
                date=availability_datetime,
                available=True,
            )

            availabiliies.append(availability)

        psychologist.add_availabilities(availabiliies)

        updated_psychologist = await self.psychologist_repo.update(psychologist)
        return PsychologistDTO.to_dto(updated_psychologist)
