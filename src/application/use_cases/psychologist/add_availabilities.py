from datetime import datetime, timezone
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
            # DEBUG
            print(
                f"DEBUG - Received datetime: {availability_datetime}, hour: {availability_datetime.hour}"
            )

            if availability_datetime < datetime.now(timezone.utc):
                raise ApplicationException(
                    "Não é possível adicionar disponibilidade em uma data passada."
                )
            # Validate that the time is a whole hour (minutes and seconds zero)
            if (
                availability_datetime.minute != 0
                or availability_datetime.second != 0
                or availability_datetime.microsecond != 0
            ):
                raise ApplicationException(
                    "Availabilities must be on whole hours (e.g. 05:00, 14:00)."
                )

            # Validate hour range: 05:00 through 23:00 inclusive
            # NOTE: Hours are in UTC, so we need to allow 0-2 (which are 21-23 in BRT UTC-3)
            if not (
                (5 <= availability_datetime.hour <= 23)
                or (0 <= availability_datetime.hour <= 2)
            ):
                print(f"DEBUG - Rejecting hour: {availability_datetime.hour}")
                raise ApplicationException(
                    "Availabilities must be between 05:00 and 23:00 inclusive."
                )

            availability = Availability(
                date=availability_datetime,
                available=True,
            )

            availabiliies.append(availability)

        psychologist.add_availabilities(availabiliies)

        updated_psychologist = await self.psychologist_repo.update(psychologist)
        return PsychologistDTO.to_dto(updated_psychologist)
