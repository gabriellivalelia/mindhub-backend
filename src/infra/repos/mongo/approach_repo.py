import asyncio

from beanie.operators import In
from pymongo import ASCENDING, DESCENDING
from pymongo.asynchronous.client_session import AsyncClientSession

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.approach_filters import ApproachFilters
from application.repos.iapproach_repo import IApproachRepo
from domain.approach import Approach
from domain.common.unique_entity_id import UniqueEntityId
from infra.mappers.mongo.approach_mapper import ApproachMongoMapper
from infra.models.mongo.approach_document import ApproachDocument


class MongoApproachRepo(IApproachRepo):
    _session: AsyncClientSession

    def __init__(self, session: AsyncClientSession) -> None:
        self._session = session

    async def create(self, entity: Approach) -> Approach:
        doc = await ApproachMongoMapper.to_model(entity)
        await doc.save(session=self._session)
        return await ApproachMongoMapper.to_domain(doc)

    async def get_by_id(self, id: UniqueEntityId) -> Approach | None:
        doc = await ApproachDocument.find_one(ApproachDocument.id == id.value, session=self._session)
        return await ApproachMongoMapper.to_domain(doc) if doc else None

    async def get_by_ids(self, ids: list[UniqueEntityId]) -> list[Approach]:
        docs = await ApproachDocument.find(
            In(ApproachDocument.id, [id.value for id in ids]), session=self._session
        ).to_list()

        return await asyncio.gather(*(ApproachMongoMapper.to_domain(doc) for doc in docs))

    async def get(
        self,
        pageable: Pageable,
        filters: ApproachFilters | None = None,
    ) -> Page[Approach]:
        query_conditions = {}

        if filters:
            if filters.name:
                query_conditions["name"] = {"$regex": filters.name, "$options": "i"}

        find_query = ApproachDocument.find(
            query_conditions if query_conditions else {},
            session=self._session,
        )
        total = await find_query.count()

        if pageable.sort:
            direction_dict = {"asc": ASCENDING, "desc": DESCENDING}
            sort_list = [(field_name, direction_dict[direction.value]) for field_name, direction in pageable.sort]
            find_query = find_query.sort(sort_list)  # type: ignore
        else:
            find_query = find_query.sort([("name", 1)])  # type: ignore (default: alphabetical)

        find_query = find_query.skip(pageable.offset()).limit(pageable.limit())
        docs = await find_query.to_list()

        entities = await asyncio.gather(*(ApproachMongoMapper.to_domain(doc) for doc in docs))

        return Page(
            items=entities,
            total=total,
            pageable=pageable,
        )
