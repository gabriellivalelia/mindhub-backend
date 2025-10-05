from domain.common.unique_entity_id import UniqueEntityId
from domain.specialty import Specialty
from infra.mappers.imapper import IMapper
from infra.models.mongo.specialty_document import SpecialtyDocument


class SpecialtyMongoMapper(IMapper[SpecialtyDocument, Specialty]):
    @staticmethod
    async def to_domain(model: SpecialtyDocument) -> Specialty:
        return Specialty(
            name=model.name,
            description=model.description,
            id=UniqueEntityId(model.id),
        )

    @staticmethod
    async def to_model(entity: Specialty) -> SpecialtyDocument:
        return SpecialtyDocument(
            id=entity.id.value,
            name=entity.name,
            description=entity.description,
        )
