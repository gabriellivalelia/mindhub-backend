from __future__ import annotations

from application.dtos.availability_dto import AvailabilityDTO
from application.dtos.city_dto import CityDTO
from application.dtos.specialty_dto import SpecialtyDTO
from application.dtos.user_dto import UserDTO
from domain.psychologist import Psychologist


class PsychologistDTO(UserDTO):
    crp: str
    description: str
    specialties: list[SpecialtyDTO]
    approaches: list[str]
    audiences: list[str]
    availabilities: list[AvailabilityDTO] | None = None

    @staticmethod
    def to_dto(entity: Psychologist) -> PsychologistDTO:
        return PsychologistDTO(
            id=entity.id.value,
            name=entity.name,
            email=entity.email.value,
            cpf=entity.cpf.value,
            phone_number=entity.phone_number.value,
            birth_date=entity.birth_date,
            gender=entity.gender,
            crp=entity.crp.value,
            description=entity.description,
            specialties=[SpecialtyDTO.to_dto(s) for s in entity.specialties],
            approaches=[approach.value for approach in entity.approaches],
            audiences=[audience.value for audience in entity.audiences],
            city=CityDTO.to_dto(entity.city),
            profile_picture=entity.profile_picture,
            availabilities=[
                AvailabilityDTO.to_dto(availability)
                for availability in entity.availabilities
            ]
            if entity.availabilities
            else None,
        )
