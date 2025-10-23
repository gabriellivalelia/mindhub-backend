import asyncio

# uuid.UUID not required here
from beanie import WriteRules
from beanie.operators import In
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

    async def create(self, entity: Psychologist) -> Psychologist:
        doc = await PsychologistMongoMapper.to_model(entity)
        await doc.save(link_rule=WriteRules.WRITE, session=self._session)
        await doc.fetch_all_links()

        return await PsychologistMongoMapper.to_domain(doc)

    async def update(self, entity: Psychologist) -> Psychologist:
        doc = await PsychologistMongoMapper.to_model(entity)
        await doc.save(link_rule=WriteRules.WRITE, session=self._session)
        await doc.fetch_all_links()

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
        filters_exprs: list[object] = []

        if filters:
            if filters.name:
                # case-insensitive regex match for name
                filters_exprs.append(
                    {"name": {"$regex": filters.name, "$options": "i"}}
                )
            if filters.gender is not None:
                filters_exprs.append(
                    PsychologistDocument.gender == filters.gender.value
                )
            if filters.specialty_ids is not None:
                filters_exprs.append(
                    In(PsychologistDocument.specialties.id, list(filters.specialty_ids))
                )
            if filters.approach_ids is not None:
                filters_exprs.append(
                    In(PsychologistDocument.approaches.id, list(filters.approach_ids))
                )
            if filters.audiences:
                filters_exprs.append(
                    In(
                        PsychologistDocument.audiences,
                        [a.value for a in filters.audiences],
                    )
                )
            if filters.max_price is not None:
                filters_exprs.append(
                    PsychologistDocument.value_per_appointment <= filters.max_price
                )

        find_query = PsychologistDocument.find(
            *filters_exprs if filters_exprs else {},
            fetch_links=True,
            session=self._session,
        )
        total = await PsychologistDocument.find(
            *filters_exprs if filters_exprs else {}, session=self._session
        ).count()

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
