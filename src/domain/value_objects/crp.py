import re

from pydantic import field_validator

from domain.common.exception import DomainException
from domain.common.value_object import ValueObject


class CRP(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def validate_crp(cls, v: str):
        pattern = r"^\d{2}/\d{4,5}$"
        crp = v.strip()
        if not re.match(pattern, crp):
            raise DomainException("Formato de CRP inválido. Formato esperado: XX/XXXX ou XX/XXXXX")

        return crp
