import asyncio

from beanie import WriteRules
from beanie.operators import In
from pymongo import ASCENDING, DESCENDING
from pymongo.asynchronous.client_session import AsyncClientSession

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.specialty_filters import SpecialtyFilters
from application.repos.ispecialty_repo import ISpecialtyRepo
from domain.common.unique_entity_id import UniqueEntityId
from domain.specialty import Specialty
from infra.mappers.mongo.specialty_mapper import SpecialtyMongoMapper
from infra.models.mongo.specialty_document import SpecialtyDocument


class MongoSpecialtyRepo(ISpecialtyRepo):
    _session: AsyncClientSession

    def __init__(self, session: AsyncClientSession) -> None:
        self._session = session

    async def create(self, entity: Specialty) -> Specialty:
        doc = await SpecialtyMongoMapper.to_model(entity)
        await doc.save(link_rule=WriteRules.WRITE, session=self._session)

        return await SpecialtyMongoMapper.to_domain(doc)

    async def get_by_id(self, id: UniqueEntityId) -> Specialty | None:
        doc = await SpecialtyDocument.find_one(SpecialtyDocument.id == id.value, session=self._session)

        return await SpecialtyMongoMapper.to_domain(doc) if doc else None

    async def get_by_ids(self, ids: list[UniqueEntityId]) -> list[Specialty]:
        docs = await SpecialtyDocument.find(
            In(SpecialtyDocument.id, [id.value for id in ids]), session=self._session
        ).to_list()
        return await asyncio.gather(*(SpecialtyMongoMapper.to_domain(doc) for doc in docs))

    async def get_all(self) -> list[Specialty]:
        docs = await SpecialtyDocument.find_all(session=self._session).to_list()
        return await asyncio.gather(*(SpecialtyMongoMapper.to_domain(doc) for doc in docs))

    async def get(self, pageable: Pageable, filters: SpecialtyFilters) -> Page[Specialty]:
        query_conditions = {}

        if filters.name:
            query_conditions["name"] = {"$regex": filters.name, "$options": "i"}

        find_query = SpecialtyDocument.find(
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

        entities = await asyncio.gather(*(SpecialtyMongoMapper.to_domain(doc) for doc in docs))

        return Page(
            items=entities,
            total=total,
            pageable=pageable,
        )
