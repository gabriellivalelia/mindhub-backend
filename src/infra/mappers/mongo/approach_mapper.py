from domain.approach import Approach
from domain.common.unique_entity_id import UniqueEntityId
from infra.mappers.imapper import IMapper
from infra.models.mongo.approach_document import ApproachDocument


class ApproachMongoMapper(IMapper[ApproachDocument, Approach]):
    @staticmethod
    async def to_domain(model: ApproachDocument) -> Approach:
        return Approach(
            name=model.name,
            description=model.description,
            id=UniqueEntityId(model.id) if model.id else None,
        )

    @staticmethod
    async def to_model(entity: Approach) -> ApproachDocument:
        return ApproachDocument(
            id=entity.id.value,
            name=entity.name,
            description=entity.description,
        )
