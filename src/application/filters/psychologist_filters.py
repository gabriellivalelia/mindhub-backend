from typing import Annotated, Any, Iterable
from uuid import UUID

from pydantic import BaseModel, BeforeValidator


def convert_empty_str_to_none(value: Any) -> Any:
    if value == "" or (isinstance(value, Iterable) and all(s == "" for s in value)):  # type: ignore
        return None

    return value  # type: ignore


ConvertEmptyStrToNoneBeforeValidator = BeforeValidator(convert_empty_str_to_none)


class PsychologistFilters(BaseModel):
    name: Annotated[str | None, ConvertEmptyStrToNoneBeforeValidator] = None
    email: Annotated[str | None, ConvertEmptyStrToNoneBeforeValidator] = None
    city_id: UUID | None = None
    state_id: UUID | None = None
    specialty_ids: set[UUID] | None = None
    approach_ids: set[UUID] | None = None
    audiences: Annotated[set[str] | None, ConvertEmptyStrToNoneBeforeValidator] = None
    min_price: float | None = None
    max_price: float | None = None

    class Config:
        extra = "forbid"
