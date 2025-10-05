from domain.city import City
from domain.common.unique_entity_id import UniqueEntityId
from infra.mappers.imapper import IMapper
from infra.mappers.mongo.state_mapper import StateMongoMapper
from infra.models.mongo.city_document import CityDocument


class CityMongoMapper(IMapper[CityDocument, City]):
    @staticmethod
    async def to_domain(model: CityDocument) -> City:
        state = await StateMongoMapper.to_domain(model.state)

        return City(
            name=model.name,
            state=state,
            id=UniqueEntityId(model.id),
        )

    @staticmethod
    async def to_model(entity: City) -> CityDocument:
        return CityDocument(
            name=entity.name,
            state=entity.state.id.value,
            id=entity.id.value,
        )
