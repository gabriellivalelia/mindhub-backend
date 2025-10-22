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
        query_conditions = {}

        # Flags para saber se precisamos filtrar em memória (campos com Links)
        needs_memory_filter = False

        if filters:
            if filters.name:
                query_conditions["name"] = {"$regex": filters.name, "$options": "i"}
            if filters.email:
                query_conditions["email"] = {"$regex": filters.email, "$options": "i"}
            if filters.audiences:
                query_conditions["audiences"] = {"$in": list(filters.audiences)}
            if filters.min_price is not None:
                query_conditions["value_per_appointment"] = {"$gte": filters.min_price}
            if filters.max_price is not None:
                if "value_per_appointment" in query_conditions:
                    query_conditions["value_per_appointment"]["$lte"] = (
                        filters.max_price
                    )
                else:
                    query_conditions["value_per_appointment"] = {
                        "$lte": filters.max_price
                    }

            # Campos com Links precisam de filtragem em memória
            if (
                filters.city_id
                or filters.state_id
                or filters.specialty_ids
                or filters.approach_ids
            ):
                needs_memory_filter = True

        # Se temos filtros de Links, precisamos filtrar em memória após fetch_links
        if needs_memory_filter:
            # Buscar todos os psicólogos que passam nos filtros simples
            all_psychologists = await PsychologistDocument.find(
                query_conditions if query_conditions else {},
                fetch_links=True,
                session=self._session,
            ).to_list()

            # Filtrar manualmente por campos Link após fetch
            filtered_psychologists = all_psychologists

            # Filtro por city_id
            if filters.city_id:
                filtered_psychologists = [
                    p
                    for p in filtered_psychologists
                    if p.city and hasattr(p.city, "id") and p.city.id == filters.city_id
                ]

            # Filtro por state_id (via city.state)
            if filters.state_id:
                filtered_psychologists = [
                    p
                    for p in filtered_psychologists
                    if (
                        p.city
                        and hasattr(p.city, "state")
                        and p.city.state
                        and hasattr(p.city.state, "id")
                        and p.city.state.id == filters.state_id
                    )
                ]

            # Filtro por specialty_ids
            if filters.specialty_ids:
                filtered_psychologists = [
                    p
                    for p in filtered_psychologists
                    if p.specialties
                    and any(
                        hasattr(s, "id") and s.id in filters.specialty_ids
                        for s in p.specialties
                    )
                ]

            # Filtro por approach_ids
            if filters.approach_ids:
                filtered_psychologists = [
                    p
                    for p in filtered_psychologists
                    if p.approaches
                    and any(
                        hasattr(a, "id") and a.id in filters.approach_ids
                        for a in p.approaches
                    )
                ]

            total = len(filtered_psychologists)

            # Aplicar ordenação
            if pageable.sort:
                # Ordenação manual (simplificada para nome por enquanto)
                filtered_psychologists.sort(key=lambda p: p.name)
            else:
                filtered_psychologists.sort(key=lambda p: p.name)

            # Aplicar paginação manualmente
            start = pageable.offset()
            end = start + pageable.limit()
            docs = filtered_psychologists[start:end]
        else:
            # Sem filtros de Link, podemos fazer query normal
            total = await PsychologistDocument.find(
                query_conditions if query_conditions else {}, session=self._session
            ).count()

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
