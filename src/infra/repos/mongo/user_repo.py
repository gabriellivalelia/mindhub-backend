from pymongo.asynchronous.client_session import AsyncClientSession

from application.common.exception import ApplicationException
from application.repos.iuser_repo import IUserRepo
from domain.common.unique_entity_id import UniqueEntityId
from domain.user import User
from infra.mappers.mongo.user_mapper import UserMongoMapper
from infra.models.mongo.user_document import UserDocument


class MongoUserRepo(IUserRepo):
    _session: AsyncClientSession

    def __init__(self, session: AsyncClientSession) -> None:
        self._session = session

    async def exists_by_email_or_cpf(
        self, email: str | None = None, cpf: str | None = None
    ) -> bool:
        if not email or not cpf:
            raise ApplicationException("Invalid cpf and email.")

        query: list[dict[str, str]] = []
        if email:
            query.append({"email": email})
        if cpf:
            query.append({"cpf": cpf})

        docs_num = await UserDocument.find_one(
            {"$or": query},
            session=self._session,
            with_children=True,
        ).count()

        return docs_num > 0

    async def get_by_id(self, user_id: UniqueEntityId) -> User | None:
        found_doc = await UserDocument.get(
            user_id.value,
            fetch_links=True,
            session=self._session,
            with_children=True,
        )
        if found_doc is None:
            return None

        await found_doc.fetch_all_links()
        return await UserMongoMapper.to_domain(found_doc)

    async def get_by_email(self, email: str) -> User | None:
        found_doc = await UserDocument.find_one(
            {"email": email},
            fetch_links=True,
            session=self._session,
            with_children=True,
        )
        if found_doc is None:
            return None

        await found_doc.fetch_all_links()
        return await UserMongoMapper.to_domain(found_doc)
