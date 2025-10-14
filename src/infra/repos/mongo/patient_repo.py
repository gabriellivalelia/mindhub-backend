import asyncio
from datetime import datetime

from beanie import WriteRules
from pymongo import ASCENDING, DESCENDING
from pymongo.asynchronous.client_session import AsyncClientSession

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.patient_filters import PatientFilters
from application.repos.ipatient_repo import IPatientRepo
from domain.appointment import Appointment
from domain.common.unique_entity_id import UniqueEntityId
from domain.patient import Patient
from infra.mappers.mongo.patient_mapper import PatientMongoMapper
from infra.models.mongo.patient_document import PatientDocument


class MongoPatientRepo(IPatientRepo):
    _session: AsyncClientSession

    def __init__(self, session: AsyncClientSession) -> None:
        self._session = session

    async def exists_by_email_or_cpf(self, email: str, cpf: str) -> bool:
        docs_num = await PatientDocument.find_one(
            {"$or": [{"email": email}, {"cpf": cpf}]}, session=self._session
        ).count()

        return docs_num > 0

    async def create(self, entity: Patient) -> Patient:
        doc = await PatientMongoMapper.to_model(entity)
        await doc.save(link_rule=WriteRules.WRITE, session=self._session)
        await doc.fetch_all_links()

        return await PatientMongoMapper.to_domain(doc)

    async def update(self, entity: Patient) -> Patient:
        doc = await PatientMongoMapper.to_model(entity)
        await doc.save(link_rule=WriteRules.WRITE, session=self._session)
        await doc.fetch_all_links()

        return await PatientMongoMapper.to_domain(doc)

    async def get_by_id(self, id: UniqueEntityId) -> Patient | None:
        doc = await PatientDocument.find_one(
            PatientDocument.id == id.value, fetch_links=True, session=self._session
        )

        return await PatientMongoMapper.to_domain(doc) if doc else None

    async def get(
        self,
        pageable: Pageable,
        filters: PatientFilters | None = None,
    ) -> Page[Patient]:
        query_conditions = {}

        if filters:
            if filters.name:
                query_conditions["name"] = {"$regex": filters.name, "$options": "i"}
            if filters.email:
                query_conditions["email"] = {"$regex": filters.email, "$options": "i"}

        total = await PatientDocument.count()

        find_query = PatientDocument.find(
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
            *(PatientMongoMapper.to_domain(doc) for doc in docs)
        )
        return Page(
            items=entities,
            total=total,
            pageable=pageable,
        )

    async def delete(self, id: UniqueEntityId) -> bool:
        doc = await PatientDocument.find_one(
            PatientDocument.id == id.value, session=self._session
        )
        if doc:
            await doc.delete(session=self._session)
            return True
        return False

    async def schedule_appointment(
        self, entity: Patient, date: datetime, psychologist_id: UniqueEntityId
    ) -> Appointment | None:
        raise NotImplementedError()
