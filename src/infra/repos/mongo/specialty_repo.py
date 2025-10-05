import asyncio

from beanie import WriteRules
from beanie.operators import In
from pymongo.asynchronous.client_session import AsyncClientSession

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
        doc = await SpecialtyDocument.find_one(
            SpecialtyDocument.id == id.value, session=self._session
        )

        return await SpecialtyMongoMapper.to_domain(doc) if doc else None

    async def get_by_ids(self, ids: list[UniqueEntityId]) -> list[Specialty]:
        docs = await SpecialtyDocument.find(
            In(SpecialtyDocument.id, [id.value for id in ids]), session=self._session
        ).to_list()
        return await asyncio.gather(
            *(SpecialtyMongoMapper.to_domain(doc) for doc in docs)
        )

    async def get_all(self) -> list[Specialty]:
        docs = await SpecialtyDocument.find_all(session=self._session).to_list()
        return await asyncio.gather(
            *(SpecialtyMongoMapper.to_domain(doc) for doc in docs)
        )
