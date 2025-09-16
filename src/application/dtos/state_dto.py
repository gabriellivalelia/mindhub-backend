from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, FieldSerializationInfo, field_serializer

from domain.state import State


class StateDTO(BaseModel):
    id: UUID
    name: str
    abbreviation: str

    @field_serializer("id")
    def serialize_dt(self, id: UUID, _info: FieldSerializationInfo):
        return str(id)

    @staticmethod
    def to_dto(entity: State) -> StateDTO:
        return StateDTO(
            id=entity.id.value, name=entity.name, abbreviation=entity.abbreviation
        )
