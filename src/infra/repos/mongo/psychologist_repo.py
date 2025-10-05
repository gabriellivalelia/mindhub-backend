import asyncio

from beanie import WriteRules
from pymongo import ASCENDING, DESCENDING
from pymongo.asynchronous.client_session import AsyncClientSession

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.psychologist_filters import PsychologistFilters
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.common.unique_entity_id import UniqueEntityId
from domain.psychologist import Psychologist
from infra.mappers.mongo.psychologist_mapper import PsychologistMongoMapper
from infra.models.mongo.psychologist_document import PsychologistDocument


class MongoPsychologistRepo(IPsychologistRepo):
    _session: AsyncClientSession

    def __init__(self, session: AsyncClientSession) -> None:
        self._session = session

    async def exists_by_crp(self, crp: str) -> bool:
        docs_num = await PsychologistDocument.find_one(
            {"crp": crp},
            session=self._session,
        ).count()

        return docs_num > 0

    async def create(self, entity: Psychologist) -> Psychologist:
        doc = await PsychologistMongoMapper.to_model(entity)
        await doc.save(link_rule=WriteRules.WRITE, session=self._session)
        await doc.fetch_all_links()

        return await PsychologistMongoMapper.to_domain(doc)

    async def update(self, entity: Psychologist) -> Psychologist:
        doc = await PsychologistMongoMapper.to_model(entity)
        await doc.save(link_rule=WriteRules.WRITE, session=self._session)
        await doc.fetch_all_links()
        # ex = await AvailabilityDocument.find_all(session=self._session).to_list()

        return await PsychologistMongoMapper.to_domain(doc)

    async def get_by_id(self, id: UniqueEntityId) -> Psychologist | None:
        doc = await PsychologistDocument.find_one(
            PsychologistDocument.id == id.value, fetch_links=True, session=self._session
        )

        return await PsychologistMongoMapper.to_domain(doc) if doc else None

    async def get(
        self,
        pageable: Pageable,
        filters: PsychologistFilters | None = None,
    ) -> Page[Psychologist]:
        query_conditions = {}

        if filters:
            if filters.name:
                query_conditions["name"] = {"$regex": filters.name, "$options": "i"}
            if filters.email:
                query_conditions["email"] = {"$regex": filters.email, "$options": "i"}
            if filters.city_id:
                query_conditions["city"] = filters.city_id
            if filters.specialty_ids:
                query_conditions["specialties"] = {"$in": list(filters.specialty_ids)}
            if filters.approaches:
                query_conditions["approaches"] = {"$in": list(filters.approaches)}
            if filters.audiences:
                query_conditions["audiences"] = {"$in": list(filters.audiences)}

        total = await PsychologistDocument.count()

        find_query = PsychologistDocument.find(
            query_conditions if query_conditions else {},
            fetch_links=True,
            session=self._session,
        )

        if pageable.sort:
            direction_dict = {"asc": ASCENDING, "desc": DESCENDING}
            sort_list = [
                (field_name, direction_dict[direction.value])
                for field_name, direction in pageable.sort
            ]
            find_query = find_query.sort(sort_list)  # type: ignore
        else:
            find_query = find_query.sort([("name", 1)])  # type: ignore

        find_query = find_query.skip(pageable.offset()).limit(pageable.limit())
        docs = await find_query.to_list()

        entities = await asyncio.gather(
            *(PsychologistMongoMapper.to_domain(doc) for doc in docs)
        )

        return Page(
            items=entities,
            total=total,
            pageable=pageable,
        )
