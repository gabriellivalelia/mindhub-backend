from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, FieldSerializationInfo, field_serializer

from domain.approach import Approach


class ApproachDTO(BaseModel):
    id: UUID
    name: str

    @field_serializer("id")
    def serialize_dt(self, id: UUID, _info: FieldSerializationInfo):
        return str(id)

    @staticmethod
    def to_dto(entity: Approach) -> ApproachDTO:
        return ApproachDTO(id=entity.id.value, name=entity.name)
