from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, FieldSerializationInfo, field_serializer

from application.dtos.state_dto import StateDTO
from domain.city import City


class CityDTO(BaseModel):
    id: UUID
    name: str
    state: StateDTO

    @field_serializer("id")
    def serialize_dt(self, id: UUID, _info: FieldSerializationInfo):
        return str(id)

    @staticmethod
    def to_dto(entity: City) -> CityDTO:
        return CityDTO(
            id=entity.id.value,
            name=entity.name,
            state=StateDTO.to_dto(entity.state),
        )
