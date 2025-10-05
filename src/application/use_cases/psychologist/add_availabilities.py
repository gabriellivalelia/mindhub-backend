from datetime import datetime
from uuid import UUID

from application.common.use_case import IUseCase
from application.dtos.psychologist_dto import PsychologistDTO
from application.repos.iavailability_repo import IAvailabilityRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.availability import Availability
from domain.common.exception import DomainException
from domain.common.unique_entity_id import UniqueEntityId
from pydantic import BaseModel


class AddAvailabilitiesDTO(BaseModel):
    availability_datetimes: list[datetime]
    psychologist_id: UUID

    class Config:
        arbitrary_types_allowed = True


class AddAvailabilitiesUseCase(IUseCase[AddAvailabilitiesDTO, PsychologistDTO]):
    psychologist_repo: IPsychologistRepo
    availability_repo: IAvailabilityRepo

    def __init__(
        self,
        psychologist_repo: IPsychologistRepo,
        availability_repo: IAvailabilityRepo,
    ) -> None:
        self.psychologist_repo = psychologist_repo
        self.availability_repo = availability_repo

    async def execute(self, dto: AddAvailabilitiesDTO) -> PsychologistDTO:
        availability_datetimes = dto.availability_datetimes

        if not availability_datetimes:
            raise DomainException("No availability datetimes provided.")

        psychologist = await self.psychologist_repo.get_by_id(
            UniqueEntityId(dto.psychologist_id)
        )

        if not psychologist:
            raise DomainException("Psychologist not found.")

        created_availabilities = []

        for availability_datetime in availability_datetimes:
            availability = Availability(
                date=availability_datetime,
                available=True,
                appointment_id=None,
            )
            created_availability = await self.availability_repo.save(availability)
            created_availabilities.append(created_availability)

        await self.psychologist_repo.add_availabilities(
            dto.entity,
            [availability.id for availability in created_availabilities],
        )

        updated_psychologist = await self.psychologist_repo.get_by_id(dto.entity.id)
        if updated_psychologist is None:
            raise DomainException("Psychologist not found after update.")

        return PsychologistDTO.to_dto(updated_psychologist)
