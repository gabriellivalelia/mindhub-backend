from domain.city import City
from domain.common.unique_entity_id import UniqueEntityId
from infra.mappers.imapper import IMapper
from infra.mappers.mongo.state_mapper import StateMongoMapper
from infra.models.mongo.city_document import CityDocument


class CityMongoMapper(IMapper[CityDocument, City]):
    @staticmethod
    async def to_domain(model: CityDocument) -> City:
        state = await StateMongoMapper.to_domain(model.state)  # type: ignore

        return City(
            name=model.name,
            state=state,
            id=UniqueEntityId(model.id),
        )

    @staticmethod
    async def to_model(entity: City) -> CityDocument:
        state = await StateMongoMapper.to_model(entity.state)

        return CityDocument(
            name=entity.name,
            state=state,  # type: ignore
            id=entity.id.value,
        )
