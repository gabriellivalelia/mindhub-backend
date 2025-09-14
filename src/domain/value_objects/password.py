from pydantic import ValidationInfo, field_validator

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
    value: str
    hashed: bool = False

    @field_validator("value")
    @classmethod
    def validate_password(cls, v: str, info: ValidationInfo):
        # Skip validation if already hashed
        if info.data.get("hashed", False):
            return v

        if len(v) < MIN_LENGTH or len(v) > MAX_LENGTH:
            raise DomainException(
                f"Password length must be between {MIN_LENGTH} and {MAX_LENGTH} characters"
            )

        if INCLUDES_NUMBERS and not any(c.isdigit() for c in v):
            raise DomainException("Password must include at least one numeral")

        if INCLUDES_UPPERCASE and not any(c.isupper() for c in v):
            raise DomainException("Password must include at least one uppercase letter")

        if INCLUDES_LOWERCASE and not any(c.islower() for c in v):
            raise DomainException("Password must include at least one lowercase letter")

        if INCLUDES_SPECIAL_CHARS and not any(c in SPECIAL_CHARS for c in v):
            raise DomainException(
                f"Password must include at least one special character: "
                f"{''.join(sorted(SPECIAL_CHARS))}"
            )

        return v
