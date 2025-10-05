from pymongo.asynchronous.client_session import AsyncClientSession

from application.repos.iuser_repo import IUserRepo
from domain.common.unique_entity_id import UniqueEntityId
from domain.user import User
from infra.mappers.mongo.user_mapper import UserMongoMapper
from infra.models.mongo.user_document import UserDocument


class MongoUserRepo(IUserRepo):
    _session: AsyncClientSession

    def __init__(self, session: AsyncClientSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UniqueEntityId) -> User | None:
        found_doc = await UserDocument.get(
            user_id.value,
            fetch_links=True,
            session=self._session,
            with_children=True,
        )

        return await UserMongoMapper.to_domain(found_doc) if found_doc else None

    async def get_by_email(self, email: str) -> User | None:
        found_doc = await UserDocument.find_one(
            {"email": email},
            fetch_links=True,
            session=self._session,
            with_children=True,
        )

        return await UserMongoMapper.to_domain(found_doc) if found_doc else None
