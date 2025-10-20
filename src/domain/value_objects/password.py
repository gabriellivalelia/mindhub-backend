from __future__ import annotations

from pydantic import Field, ValidationInfo, field_validator

from domain.common.exception import DomainException
from domain.common.value_object import ValueObject

SPECIAL_CHARS = set("$@#%!^&*()-_+=")

MIN_LENGTH: int = 6
MAX_LENGTH: int = 20
INCLUDES_SPECIAL_CHARS: bool = True
INCLUDES_NUMBERS: bool = True
INCLUDES_LOWERCASE: bool = True
INCLUDES_UPPERCASE: bool = True


class Password(ValueObject):
    hashed: bool = Field(default=False)
    value: str

    @field_validator("value", mode="after")
    @classmethod
    def validate_password(cls, v: str, info: ValidationInfo):
        # Skip validation if already hashed
        if info.data.get("hashed", False):
            return v

        if len(v) < MIN_LENGTH or len(v) > MAX_LENGTH:
            raise DomainException(
                f"A senha deve ter entre {MIN_LENGTH} e {MAX_LENGTH} caracteres"
            )

        if INCLUDES_NUMBERS and not any(c.isdigit() for c in v):
            raise DomainException("A senha deve incluir pelo menos um número")

        if INCLUDES_UPPERCASE and not any(c.isupper() for c in v):
            raise DomainException("A senha deve incluir pelo menos uma letra maiúscula")

        if INCLUDES_LOWERCASE and not any(c.islower() for c in v):
            raise DomainException("A senha deve incluir pelo menos uma letra minúscula")

        if INCLUDES_SPECIAL_CHARS and not any(c in SPECIAL_CHARS for c in v):
            raise DomainException(
                f"A senha deve incluir pelo menos um caractere especial: "
                f"{''.join(sorted(SPECIAL_CHARS))}"
            )

        return v
