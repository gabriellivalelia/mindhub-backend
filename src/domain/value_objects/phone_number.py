import re

from pydantic import field_validator

from domain.common.exception import DomainException
from domain.common.value_object import ValueObject

brazilian_phone_number_pattern = r"^(\+55\s?)?(\(?\d{2}\)?\s?)?9?\d{4}-?\d{4}$"


class PhoneNumber(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def validate_phone_number(cls, v: str):
        phone = v.strip()
        if not re.match(brazilian_phone_number_pattern, phone):
            raise DomainException("Formato de número de telefone brasileiro inválido")
        return phone
