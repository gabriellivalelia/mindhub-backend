from domain.availability import Availability
from domain.common.unique_entity_id import UniqueEntityId
from infra.mappers.imapper import IMapper
from infra.models.mongo.availability_document import AvailabilityDocument


class AvailabilityMongoMapper(IMapper[AvailabilityDocument, Availability]):
    @staticmethod
    async def to_domain(model: AvailabilityDocument) -> Availability:
        return Availability(
            date=model.date,
            available=model.available,
            id=UniqueEntityId(model.id),
        )

    @staticmethod
    async def to_model(entity: Availability) -> AvailabilityDocument:
        return AvailabilityDocument(
            id=entity.id.value,
            date=entity.date,
            available=entity.available,
        )
