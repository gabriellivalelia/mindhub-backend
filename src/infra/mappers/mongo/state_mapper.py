from domain.common.unique_entity_id import UniqueEntityId
from domain.state import State
from infra.mappers.imapper import IMapper
from infra.models.mongo.state_document import StateDocument


class StateMongoMapper(IMapper[StateDocument, State]):
    @staticmethod
    async def to_domain(model: StateDocument) -> State:
        return State(
            name=model.name,
            abbreviation=model.abbreviation,
            id=UniqueEntityId(model.id),
        )

    @staticmethod
    async def to_model(entity: State) -> StateDocument:
        return StateDocument(
            name=entity.name,
            abbreviation=entity.abbreviation,
            id=entity.id.value,
        )
