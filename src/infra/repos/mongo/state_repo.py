import asyncio

from beanie import WriteRules
from pymongo.asynchronous.client_session import AsyncClientSession

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.state_filters import StateFilters
from application.repos.istate_repo import IStateRepo
from domain.common.unique_entity_id import UniqueEntityId
from domain.state import State
from infra.mappers.mongo.state_mapper import StateMongoMapper
from infra.models.mongo.state_document import StateDocument


class MongoStateRepo(IStateRepo):
    _session: AsyncClientSession

    def __init__(self, session: AsyncClientSession) -> None:
        self._session = session

    async def create(self, entity: State) -> State:
        doc = await StateMongoMapper.to_model(entity)
        await doc.insert(link_rule=WriteRules.WRITE, session=self._session)

        return await StateMongoMapper.to_domain(doc)

    async def get_by_id(self, id: UniqueEntityId) -> State | None:
        doc = await StateDocument.find_one(StateDocument.id == id.value, session=self._session)
        return await StateMongoMapper.to_domain(doc) if doc else None

    async def get(
        self,
        pageable: Pageable,
        filters: StateFilters | None = None,
    ) -> Page[State]:
        query_conditions = {}

        if filters:
            if filters.name:
                query_conditions["name"] = {"$regex": filters.name, "$options": "i"}

        find_query = StateDocument.find(
            query_conditions if query_conditions else {},
            fetch_links=True,
            session=self._session,
        )
        total = await find_query.count()

        if pageable.sort:
            direction_dict = {"asc": 1, "desc": -1}
            sort_list = [(field_name, direction_dict[direction.value]) for field_name, direction in pageable.sort]
            find_query = find_query.sort(sort_list)  # type: ignore
        else:
            find_query = find_query.sort([("name", 1)])  # type: ignore

        find_query = find_query.skip(pageable.offset()).limit(pageable.limit())

        docs = await find_query.to_list()
        entities = await asyncio.gather(*(StateMongoMapper.to_domain(doc) for doc in docs))

        return Page(
            items=entities,
            total=total,
            pageable=pageable,
        )

    async def get_all(self) -> list[State]:
        docs = await StateDocument.find_all(fetch_links=True, session=self._session).to_list()
        return await asyncio.gather(*(StateMongoMapper.to_domain(doc) for doc in docs))
