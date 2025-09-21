from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, FieldSerializationInfo, field_serializer

from application.dtos.city_dto import CityDTO
from domain.patient import Patient
from domain.value_objects.file_data import FileData


class PatientDTO(BaseModel):
    id: UUID
    name: str
    email: str
    phone_number: str
    birth_date: date
    gender: str
    city: CityDTO | None = None
    profile_picture: FileData | None = None

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info: FieldSerializationInfo) -> str:
        return str(id)

    @staticmethod
    def to_dto(entity: Patient) -> PatientDTO:
        return PatientDTO(
            id=entity.id.value,
            name=entity.name,
            email=entity.email.value,
            phone_number=entity.phone_number.value,
            birth_date=entity.birth_date,
            gender=entity.gender,
            city=CityDTO.to_dto(entity.city),
            profile_picture=entity.profile_picture,
        )
