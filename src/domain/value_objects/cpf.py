from pydantic import field_validator

from domain.common.exception import DomainException
from domain.common.value_object import ValueObject


class CPF(ValueObject):
    value: str

    @field_validator("value")
    @classmethod
    def validate_cpf(cls, v: str):
        cpf = "".join(filter(str.isdigit, v))
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            raise DomainException("Invalid CPF format")

        def calc_digit(cpf: str, length: int) -> int:
            s: int = sum(int(cpf[i]) * (length + 1 - i) for i in range(length))
            d: int = (s * 10) % 11
            return d if d < 10 else 0

        if calc_digit(cpf, 9) != int(cpf[9]) or calc_digit(cpf, 10) != int(cpf[10]):
            raise DomainException("Invalid CPF number")

        return cpf
