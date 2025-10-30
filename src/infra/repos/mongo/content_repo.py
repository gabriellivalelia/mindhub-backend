from beanie import WriteRules
from pymongo import ASCENDING, DESCENDING
from pymongo.asynchronous.client_session import AsyncClientSession

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.content_filters import ContentFilters
from application.repos.icontent_repo import IContentRepo
from domain.common.unique_entity_id import UniqueEntityId
from domain.content import Content
from infra.mappers.mongo.content_mapper import ContentMongoMapper
from infra.models.mongo.content_document import ContentDocument


class MongoContentRepo(IContentRepo):
    _session: AsyncClientSession

    def __init__(self, session: AsyncClientSession) -> None:
        self._session = session

    async def create(self, entity: Content) -> Content:
        doc = await ContentMongoMapper.to_model(entity)
        await doc.save(link_rule=WriteRules.WRITE, session=self._session)
        await doc.fetch_all_links()

        return await ContentMongoMapper.to_domain(doc)

    async def get_by_id(self, id: UniqueEntityId) -> Content | None:
        doc = await ContentDocument.find_one(ContentDocument.id == id.value, fetch_links=True, session=self._session)

        return await ContentMongoMapper.to_domain(doc) if doc else None

    async def get(self, pageable: Pageable, filters: ContentFilters | None = None) -> Page[Content]:
        find_query = ContentDocument.find(fetch_links=True, session=self._session)

        if filters:
            if filters.title:
                find_query = find_query.find({"title": {"$regex": filters.title, "$options": "i"}})
            if filters.author_id:
                find_query = find_query.find({"author_id": filters.author_id})

        total = await find_query.count()

        if pageable.sort:
            direction_dict = {"asc": ASCENDING, "desc": DESCENDING}
            sort_list = [(field_name, direction_dict[direction.value]) for field_name, direction in pageable.sort]
            find_query = find_query.sort(sort_list)  # type: ignore
        else:
            find_query = find_query.sort([("created_at", -1)])  # type: ignore

        find_query = find_query.skip(pageable.offset()).limit(pageable.limit())
        docs = await find_query.to_list()

        entities = [await ContentMongoMapper.to_domain(doc) for doc in docs]

        return Page[Content](
            items=entities,
            total=total,
            pageable=pageable,
        )

    async def update(self, entity: Content) -> Content:
        doc = await ContentMongoMapper.to_model(entity)
        await doc.save(link_rule=WriteRules.WRITE, session=self._session)
        await doc.fetch_all_links()

        return await ContentMongoMapper.to_domain(doc)

    async def delete(self, id: UniqueEntityId) -> bool:
        result = await ContentDocument.find_one(ContentDocument.id == id.value, session=self._session)
        if not result:
            return False
        await result.delete()
        return True
