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

    async def get_all(self) -> list[City]:
        docs = await CityDocument.find_all(
            fetch_links=True, session=self._session
        ).to_list()
        return await asyncio.gather(*(CityMongoMapper.to_domain(doc) for doc in docs))
