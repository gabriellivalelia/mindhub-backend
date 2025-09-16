from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, FieldSerializationInfo, field_serializer

from application.dtos.city_dto import CityDTO
from application.dtos.specialty_dto import SpecialtyDTO
from domain.psychologist import Psychologist
from domain.value_objects.file_data import FileData


class PsychologistDTO(BaseModel):
    id: UUID
    name: str
    email: str
    phone_number: str
    birth_date: date
    gender: str
    crp: str
    description: str
    specialties: list[SpecialtyDTO]
    approaches: list[str]
    audiences: list[str]
    city: CityDTO | None = None
    profile_picture: FileData | None = None

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info: FieldSerializationInfo) -> str:
        return str(id)

    @staticmethod
    def to_dto(entity: Psychologist) -> PsychologistDTO:
        print(entity.crp.value)
        return PsychologistDTO(
            id=entity.id.value,
            name=entity.name,
            email=entity.email.value,
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
        )
