from datetime import date
from typing import Annotated, Any, Iterable
from uuid import UUID

from pydantic import BaseModel, BeforeValidator


def convert_empty_str_to_none(value: Any) -> Any:
    if value == "" or (isinstance(value, Iterable) and all(s == "" for s in value)):  # type: ignore
        return None

    return value  # type: ignore


ConvertEmptyStrToNoneBeforeValidator = BeforeValidator(convert_empty_str_to_none)


class AppointmentFilters(BaseModel):
    start_date: Annotated[date | None, ConvertEmptyStrToNoneBeforeValidator] = None
    end_date: Annotated[date | None, ConvertEmptyStrToNoneBeforeValidator] = None
    psychologist_id: UUID | None = None
    patient_id: UUID | None = None
    status: str | None = None
    availability_id: UUID | None = None
