from datetime import datetime

from domain.common.unique_entity_id import UniqueEntityId
from domain.patient import Patient
from domain.value_objects.cpf import CPF
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from domain.value_objects.phone_number import PhoneNumber
from infra.mappers.imapper import IMapper
from infra.mappers.mongo.city_mapper import CityMongoMapper
from infra.models.mongo.patient_document import PatientDocument


class PatientMongoMapper(IMapper[PatientDocument, Patient]):
    @staticmethod
    async def to_domain(model: PatientDocument) -> Patient:
        city = await CityMongoMapper.to_domain(model.city)  # type: ignore
        patient = Patient(
            name=model.name,
            email=Email(value=model.email),
            password=Password(value=model.password_hash, hashed=True),
            cpf=CPF(value=model.cpf),
            phone_number=PhoneNumber(value=model.phone_number),
            birth_date=datetime.fromisoformat(model.birth_date),
            gender=model.gender,
            city=city,
            profile_picture=model.profile_picture,
            id=UniqueEntityId(model.id),
        )

        return patient

    @staticmethod
    async def to_model(entity: Patient) -> PatientDocument:
        city = await CityMongoMapper.to_model(entity.city)

        return PatientDocument(
            id=entity.id.value,
            name=entity.name,
            email=entity.email.value,
            password_hash=entity.password.value,
            cpf=entity.cpf.value,
            phone_number=entity.phone_number.value,
            birth_date=entity.birth_date.isoformat(),
            gender=entity.gender,
            profile_picture=entity.profile_picture,
            city=city,  # type: ignore
        )
