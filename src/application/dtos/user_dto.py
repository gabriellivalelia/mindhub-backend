from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, FieldSerializationInfo, field_serializer

from application.dtos.city_dto import CityDTO
from domain.value_objects.file_data import FileData


class UserDTO(BaseModel):
    id: UUID
    name: str
    email: str
    cpf: str
    phone_number: str
    birth_date: date
    gender: str
    city: CityDTO | None = None
    profile_picture: FileData | None = None

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info: FieldSerializationInfo) -> str:
        return str(id)

    @field_serializer("birth_date")
    def serialize_birth_date(
        self, birth_date: date, _info: FieldSerializationInfo
    ) -> str:
        return birth_date.isoformat()
