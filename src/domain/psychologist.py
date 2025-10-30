from datetime import date, datetime
from enum import Enum

from domain.approach import Approach
from domain.availability import Availability
from domain.city import City
from domain.common.exception import DomainException
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


class AudienceEnum(Enum):
    CHILDREN = "children"  # Crianças (0-12 anos)
    ADOLESCENTS = "adolescents"  # Adolescentes (13-17 anos)
    ADULTS = "adults"  # Adultos (26-59 anos)
    ELDERLY = "elderly"  # Idosos (60+ anos)
    COUPLES = "couples"  # Casais


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
        specialties: list[Specialty],
        approaches: list[Approach],
        audiences: list[AudienceEnum],
        value_per_appointment: float,
        description: str | None = None,
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
                {"argument": crp, "argument_name": "crp"},
            ]
        )
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
        self.value_per_appointment = value_per_appointment

    @property
    def crp(self) -> CRP:
        return self._crp

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def specialties(self) -> list[Specialty]:
        return self._specialties

    @property
    def approaches(self) -> list[Approach]:
        return self._approaches

    @property
    def audiences(self) -> list[AudienceEnum]:
        return self._audiences

    @property
    def availabilities(self) -> list[Availability] | None:
        return self._availabilities

    def add_availabilities(self, availabilities: list[Availability]) -> None:
        if self._availabilities is None:
            self._availabilities = []

        existing_datetimes = {availability.normalized_date for availability in self._availabilities}

        new_availabilities = [
            availability for availability in availabilities if availability.normalized_date not in existing_datetimes
        ]

        self._availabilities.extend(new_availabilities)

    def remove_availabilities(self, availability_datetimes: list[datetime]) -> None:
        """Remove availabilities by their datetime. Only removes if available (not scheduled)."""
        if not self._availabilities:
            raise DomainException("O psicólogo não possui disponibilidades.")

        # Normalize datetimes for comparison
        from domain.availability import Availability as AvailabilityClass

        temp_availability = AvailabilityClass(date=datetime.now(), available=True)
        normalized_datetimes = {temp_availability._normalize_datetime(dt) for dt in availability_datetimes}

        # Filter out availabilities that match the datetimes AND are available
        removed_count = 0
        new_availabilities = []
        for availability in self._availabilities:
            if availability.normalized_date in normalized_datetimes and availability.available:
                removed_count += 1
                # Skip this availability (remove it)
                continue
            new_availabilities.append(availability)

        if removed_count == 0:
            raise DomainException("Nenhuma disponibilidade válida foi encontrada para remoção.")

        self._availabilities = new_availabilities

    def get_availability_by_date(self, availability_date: datetime) -> UniqueEntityId:
        if not self.availabilities:
            raise DomainException("O psicólogo não possui disponibilidades.")

        availability = next(
            (availability for availability in self.availabilities if availability.is_date_equals_to(availability_date)),
            None,
        )

        if not availability:
            raise DomainException("Nenhuma disponibilidade encontrada para a data informada.")

        availability.schedule()

        return availability.id
