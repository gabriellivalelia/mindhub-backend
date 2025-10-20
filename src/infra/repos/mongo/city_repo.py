import asyncio

from beanie import WriteRules
from pymongo.asynchronous.client_session import AsyncClientSession

from application.repos.icity_repo import ICityRepo
from domain.city import City
from domain.common.unique_entity_id import UniqueEntityId
from infra.mappers.mongo.city_mapper import CityMongoMapper
from infra.models.mongo.city_document import CityDocument


class MongoCityRepo(ICityRepo):
    _session: AsyncClientSession

    def __init__(self, session: AsyncClientSession) -> None:
        self._session = session

    async def create(self, entity: City) -> City:
        doc = await CityMongoMapper.to_model(entity)
        await doc.save(link_rule=WriteRules.WRITE, session=self._session)

        return await CityMongoMapper.to_domain(doc)

    async def get_by_id(self, id: UniqueEntityId) -> City | None:
        doc = await CityDocument.find_one(
            CityDocument.id == id.value, fetch_links=True, session=self._session
        )
        return await CityMongoMapper.to_domain(doc) if doc else None

    async def get_all_by_state_id(self, state_id: UniqueEntityId):
        docs = await CityDocument.find(
            CityDocument.state.id == state_id.value,
            fetch_links=True,
            session=self._session,
        ).to_list()

        return await asyncio.gather(*(CityMongoMapper.to_domain(doc) for doc in docs))

    # async def get(
    #     self,
    #     pageable: Pageable,
    #     filters: CityFilters | None = None,
    # ) -> Page[City]:
    #     query_conditions = {}

    #     if filters:
    #         if filters.name:
    #             query_conditions["name"] = {"$regex": filters.name, "$options": "i"}
    #         if filters.state_id:
    #             query_conditions["state.$id"] = filters.state_id

    #     total = await CityDocument.find(
    #         query_conditions if query_conditions else {}, session=self._session
    #     ).count()

    #     find_query = CityDocument.find(
    #         query_conditions if query_conditions else {},
    #         fetch_links=True,
    #         session=self._session,
    #     )

    #     if pageable.sort:
    #         direction_dict = {"asc": ASCENDING, "desc": DESCENDING}
    #         sort_list = [
    #             (field_name, direction_dict[direction.value])
    #             for field_name, direction in pageable.sort
    #         ]
    #         find_query = find_query.sort(sort_list)  # type: ignore
    #     else:
    #         find_query = find_query.sort([("name", 1)])  # type: ignore (default: alphabetical)

    #     find_query = find_query.skip(pageable.offset()).limit(pageable.limit())
    #     docs = await find_query.to_list()

    #     entities = await asyncio.gather(
    #         *(CityMongoMapper.to_domain(doc) for doc in docs)
    #     )

    #     return Page(
    #         items=entities,
    #         total=total,
    #         pageable=pageable,
    #     )
