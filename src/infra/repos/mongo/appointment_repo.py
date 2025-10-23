import asyncio

from beanie import WriteRules
from pymongo import ASCENDING, DESCENDING
from pymongo.asynchronous.client_session import AsyncClientSession

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.appointment_filters import AppointmentFilters
from application.repos.iappointment_repo import IAppointmentRepo
from domain.appointment import Appointment
from domain.common.unique_entity_id import UniqueEntityId
from infra.mappers.mongo.appointment_mapper import AppointmentMongoMapper
from infra.models.mongo.appointment_document import AppointmentDocument


class MongoAppointmentRepo(IAppointmentRepo):
    _session: AsyncClientSession

    def __init__(self, session: AsyncClientSession) -> None:
        self._session = session

    async def create(self, entity: Appointment) -> Appointment:
        doc = await AppointmentMongoMapper.to_model(entity)
        await doc.save(link_rule=WriteRules.WRITE, session=self._session)
        await doc.fetch_all_links()

        return await AppointmentMongoMapper.to_domain(doc)

    async def get_by_id(self, id: UniqueEntityId) -> Appointment | None:
        doc = await AppointmentDocument.find_one(
            AppointmentDocument.id == id.value, fetch_links=True, session=self._session
        )

        return await AppointmentMongoMapper.to_domain(doc) if doc else None

    async def update(self, entity: Appointment) -> Appointment:
        doc = await AppointmentMongoMapper.to_model(entity)
        # save will replace the existing document with same id
        await doc.save(link_rule=WriteRules.WRITE, session=self._session)
        await doc.fetch_all_links()

        return await AppointmentMongoMapper.to_domain(doc)

    async def get(
        self,
        pageable: Pageable,
        filters: AppointmentFilters | None = None,
    ) -> Page[Appointment]:
        query_conditions = {}

        if filters:
            if filters.start_date or filters.end_date:
                date_filter = {}
                if filters.start_date:
                    date_filter["$gte"] = filters.start_date
                if filters.end_date:
                    date_filter["$lte"] = filters.end_date
                if date_filter:
                    query_conditions["date"] = date_filter

            if filters.psychologist_id:
                query_conditions["psychologist_id"] = filters.psychologist_id
            if filters.patient_id:
                query_conditions["patient_id"] = filters.patient_id
            if filters.status:
                query_conditions["status"] = filters.status
            if filters.availability_id:
                query_conditions["availability_id"] = filters.availability_id

        total = await AppointmentDocument.find(
            query_conditions if query_conditions else {}, session=self._session
        ).count()

        if pageable.sort:
            find_query = AppointmentDocument.find(
                query_conditions if query_conditions else {},
                fetch_links=True,
                session=self._session,
            )
            direction_dict = {"asc": ASCENDING, "desc": DESCENDING}
            sort_list = [
                (field_name, direction_dict[direction.value])
                for field_name, direction in pageable.sort
            ]
            find_query = find_query.sort(sort_list)  # type: ignore
            find_query = find_query.skip(pageable.offset()).limit(pageable.limit())
            docs = await find_query.to_list()
        else:
            # Default sort: canceled last, then by date descending (newest first)
            # Use aggregation pipeline for custom sorting
            pipeline = [
                {"$match": query_conditions if query_conditions else {}},
                {
                    "$addFields": {
                        "is_canceled": {
                            "$cond": {
                                "if": {"$eq": ["$status", "canceled"]},
                                "then": 1,
                                "else": 0,
                            }
                        }
                    }
                },
                {"$sort": {"is_canceled": ASCENDING, "date": DESCENDING}},
                {"$skip": pageable.offset()},
                {"$limit": pageable.limit()},
            ]

            raw_docs = await AppointmentDocument.aggregate(
                pipeline, session=self._session
            ).to_list()

            # Convert raw dicts to AppointmentDocument instances and fetch links
            docs = []
            for raw_doc in raw_docs:
                doc = await AppointmentDocument.find_one(
                    AppointmentDocument.id == raw_doc["_id"],
                    fetch_links=True,
                    session=self._session,
                )
                if doc:
                    docs.append(doc)

        entities = await asyncio.gather(
            *(AppointmentMongoMapper.to_domain(doc) for doc in docs)
        )

        return Page(
            items=entities,
            total=total,
            pageable=pageable,
        )
