from __future__ import annotations

from application.dtos.city_dto import CityDTO
from application.dtos.user_dto import UserDTO, UserType
from domain.patient import Patient


class PatientDTO(UserDTO):
    @staticmethod
    def to_dto(entity: Patient) -> PatientDTO:
        return PatientDTO(
            id=entity.id.value,
            type=UserType.PATIENT,
            name=entity.name,
            email=entity.email.value,
            phone_number=entity.phone_number.value,
            birth_date=entity.birth_date.isoformat(),
            gender=entity.gender,
            city=CityDTO.to_dto(entity.city),
            profile_picture=entity.profile_picture,
            cpf=entity.cpf.value,
        )
