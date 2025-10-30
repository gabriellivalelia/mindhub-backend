from abc import ABC
from datetime import date
from enum import Enum

from domain.city import City
from domain.common.entity import Entity
from domain.common.guard import Guard
from domain.common.unique_entity_id import UniqueEntityId
from domain.state import State
from domain.value_objects.cpf import CPF
from domain.value_objects.email import Email
from domain.value_objects.file_data import FileData
from domain.value_objects.password import Password
from domain.value_objects.phone_number import PhoneNumber


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non-binary"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


# Classe abstrata do usuário
class User(Entity, ABC):
    def __init__(
        self,
        name: str,
        email: Email | str,
        password: Password | str,
        cpf: CPF | str,
        phone_number: PhoneNumber | str,
        birth_date: date,
        gender: GenderEnum,
        city: City,
        profile_picture: FileData | None = None,
        id: UniqueEntityId | None = None,
    ) -> None:
        Guard.against_undefined_bulk(
            [
                {"argument": name, "argument_name": "name"},
                {"argument": birth_date, "argument_name": "birth_date"},
                {"argument": gender, "argument_name": "gender"},
                {"argument": city, "argument_name": "city"},
            ]
        )
        Guard.against_empty_str(name, "name")

        super().__init__(id)

        self._name = name
        self._email = email if isinstance(email, Email) else Email(value=email)
        self._password = password if isinstance(password, Password) else Password(value=password)
        self._cpf = cpf if isinstance(cpf, CPF) else CPF(value=cpf)
        self._birth_date = birth_date
        self._gender = gender
        self._phone_number = phone_number if isinstance(phone_number, PhoneNumber) else PhoneNumber(value=phone_number)
        self._profile_picture = profile_picture
        self._state = city.state
        self._city = city

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> Email:
        return self._email

    @property
    def password(self) -> Password:
        return self._password

    @property
    def cpf(self) -> CPF:
        return self._cpf

    @property
    def birth_date(self) -> date:
        return self._birth_date

    @property
    def gender(self) -> GenderEnum:
        return self._gender

    @property
    def phone_number(self) -> PhoneNumber:
        return self._phone_number

    @property
    def profile_picture(self) -> FileData | None:
        return self._profile_picture

    @property
    def state(self) -> State:
        return self._state

    @property
    def city(self) -> City:
        return self._city

    @phone_number.setter
    def phone_number(self, phone_number: str | PhoneNumber) -> None:
        self._phone_number = phone_number if isinstance(phone_number, PhoneNumber) else PhoneNumber(value=phone_number)

    @profile_picture.setter
    def profile_picture(self, profile_picture: FileData | None) -> None:
        self._profile_picture = profile_picture

    @gender.setter
    def gender(self, gender: GenderEnum) -> None:
        Guard.against_undefined(gender, "gender")
        self._gender = gender

    @city.setter
    def city(self, city: City):
        Guard.against_undefined(city, "city")
        self._city = city
