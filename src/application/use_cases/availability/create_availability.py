from datetime import datetime

from application.common.use_case import IUseCase
from application.dtos.availability_dto import AvailabilityDTO
from application.repos.iavailability_repo import IAvailabilityRepo
from domain.availability import Availability
from pydantic import BaseModel


class CreateAvailabilityDTO(BaseModel):
    date: datetime

    class Config:
        arbitrary_types_allowed = True


class CreateAvailabilityUseCase(IUseCase[CreateAvailabilityDTO, AvailabilityDTO]):
    availability_repo: IAvailabilityRepo

    def __init__(
        self,
        availabilityRepo: IAvailabilityRepo,
    ) -> None:
        self.availability_repo = availabilityRepo

    async def execute(self, dto: CreateAvailabilityDTO) -> AvailabilityDTO:
        availability = Availability(
            date=dto.date,
            available=True,
            appointment_id=None,
        )

        created_availability = await self.availability_repo.save(availability)
        return AvailabilityDTO.to_dto(created_availability)
