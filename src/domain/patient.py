from datetime import date, datetime

from domain.appointment import Appointment
from domain.city import City
from domain.common.unique_entity_id import UniqueEntityId
from domain.user import GenderEnum, User
from domain.value_objects.cpf import CPF
from domain.value_objects.email import Email
from domain.value_objects.file_data import FileData
from domain.value_objects.password import Password
from domain.value_objects.phone_number import PhoneNumber

# TODO


class Patient(User):
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

    def schedule_appointment(
        self,
        date: datetime,
        psychologist_id: UniqueEntityId,
    ) -> Appointment:
        pass

        # Ver se o horário está disponível
        # Criar o pagamento via Pix
        # Criar a consulta
        # Marcar o horário como indisponível
        # Retornar a consulta
