from datetime import date
from enum import Enum

from domain.availability import Availability
from domain.city import City
from domain.common.guard import Guard
from domain.common.unique_entity_id import UniqueEntityId
from domain.specialty import Specialty
from domain.user import GenderEnum, User
from domain.value_objects.cpf import CPF
from domain.value_objects.crp import CRP
from domain.value_objects.email import Email
from domain.value_objects.file_data import FileData
from domain.value_objects.password import Password
from domain.value_objects.phone_number import PhoneNumber


class ApproachEnum(Enum):
    TCC = "tcc"


class AudienceEnum(Enum):
    CHILDREN = "children"


class Psychologist(User):
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
        crp: CRP | str,
        description: str,
        specialties: list[Specialty],
        approaches: list[ApproachEnum],
        audiences: list[AudienceEnum],
        availabilities: list[Availability] | None = None,
        profile_picture: FileData | None = None,
        id: UniqueEntityId | None = None,
    ):
        super().__init__(
            name=name,
            email=email,
            password=password,
            cpf=cpf,
            phone_number=phone_number,
            birth_date=birth_date,
            gender=gender,
            city=city,
            profile_picture=profile_picture,
            id=id,
        )

        Guard.against_undefined_bulk(
            [
                {"argument": crp, "argument_name": "crp"},
            ]
        )
        Guard.against_empty_str(description, "description")
        Guard.against_empty_list_bulk(
            [
                {"argument": specialties, "argument_name": "specialties"},
                {"argument": approaches, "argument_name": "approaches"},
                {"argument": audiences, "argument_name": "audiences"},
            ]
        )

        self._crp = crp if isinstance(crp, CRP) else CRP(value=crp)
        self._description = description
        self._specialties = specialties
        self._approaches = approaches
        self._audiences = audiences
        self._availabilities = availabilities

    @property
    def crp(self) -> CRP:
        return self._crp

    @property
    def description(self) -> str:
        return self._description

    @property
    def specialties(self) -> list[Specialty]:
        return self._specialties

    @property
    def approaches(self) -> list[ApproachEnum]:
        return self._approaches

    @property
    def audiences(self) -> list[AudienceEnum]:
        return self._audiences

    @property
    def availabilities(self) -> list[Availability] | None:
        return self._availabilities
