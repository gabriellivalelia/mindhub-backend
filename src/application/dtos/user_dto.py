from __future__ import annotations

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
    birth_date: str
    gender: str
    city: CityDTO | None = None
    profile_picture: FileData | None = None

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info: FieldSerializationInfo) -> str:
        return str(id)
