from pydantic import EmailStr

from domain.common.value_object import ValueObject


class Email(ValueObject):
    value: EmailStr
