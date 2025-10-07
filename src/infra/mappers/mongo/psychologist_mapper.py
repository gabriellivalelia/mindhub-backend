import asyncio
from datetime import datetime

from domain.approach import Approach
from domain.availability import Availability
from domain.common.unique_entity_id import UniqueEntityId
from domain.psychologist import AudienceEnum, Psychologist
from domain.specialty import Specialty
from domain.value_objects.cpf import CPF
from domain.value_objects.crp import CRP
from domain.value_objects.email import Email
from domain.value_objects.password import Password
from domain.value_objects.phone_number import PhoneNumber
from infra.mappers.imapper import IMapper
from infra.mappers.mongo.approach_mapper import ApproachMongoMapper
from infra.mappers.mongo.availability_mapper import AvailabilityMongoMapper
from infra.mappers.mongo.city_mapper import CityMongoMapper
from infra.mappers.mongo.specialty_mapper import SpecialtyMongoMapper
from infra.models.mongo.psychologist_document import PsychologistDocument


class PsychologistMongoMapper(IMapper[PsychologistDocument, Psychologist]):
    @staticmethod
    async def to_domain(model: PsychologistDocument) -> Psychologist:
        city = await CityMongoMapper.to_domain(model.city)  # type: ignore

        specialties: list[Specialty] = [
            await SpecialtyMongoMapper.to_domain(doc)  # type: ignore
            for doc in model.specialties
        ]

        approaches: list[Approach] = [
            await ApproachMongoMapper.to_domain(doc)  # type: ignore
            for doc in model.approaches
        ]

        availabilities: list[Availability] | None = None
        if model.availabilities:
            availabilities = [
                await AvailabilityMongoMapper.to_domain(doc)  # type: ignore
                for doc in model.availabilities
            ]

        return Psychologist(
            name=model.name,
            email=Email(value=model.email),
            password=Password(value=model.password_hash, hashed=True),
            cpf=CPF(value=model.cpf),
            phone_number=PhoneNumber(value=model.phone_number),
            birth_date=datetime.fromisoformat(model.birth_date),
            gender=model.gender,
            city=city,
            crp=CRP(value=model.crp),
            description=model.description,
            specialties=specialties,
            approaches=approaches,
            audiences=[AudienceEnum(audience) for audience in model.audiences],
            value_per_appointment=model.value_per_appointment,
            availabilities=availabilities,
            profile_picture=model.profile_picture,
            id=UniqueEntityId(model.id),
        )

    @staticmethod
    async def to_model(entity: Psychologist) -> PsychologistDocument:
        availabilities = (
            await asyncio.gather(
                *(
                    AvailabilityMongoMapper.to_model(availability)
                    for availability in entity.availabilities
                )
            )
            if entity.availabilities is not None
            else None
        )
        specialties = await asyncio.gather(
            *(
                SpecialtyMongoMapper.to_model(specialty)
                for specialty in entity.specialties
            )
        )

        approaches = await asyncio.gather(
            *(ApproachMongoMapper.to_model(approach) for approach in entity.approaches)
        )

        city = await CityMongoMapper.to_model(entity.city)

        return PsychologistDocument(
            id=entity.id.value,
            name=entity.name,
            email=entity.email.value,
            password_hash=entity.password.value,
            cpf=entity.cpf.value,
            phone_number=entity.phone_number.value,
            birth_date=entity.birth_date.isoformat(),
            gender=entity.gender,
            city=city,  # type: ignore
            profile_picture=entity.profile_picture,
            crp=entity.crp.value,
            description=entity.description,
            specialties=specialties,  # type: ignore
            approaches=approaches,  # type: ignore
            audiences=[audience.value for audience in entity.audiences],
            value_per_appointment=entity.value_per_appointment,
            availabilities=availabilities,  # type: ignore
        )
