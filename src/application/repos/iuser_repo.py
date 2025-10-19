from abc import ABC, abstractmethod

from domain.common.unique_entity_id import UniqueEntityId
from domain.user import User


class IUserRepo(ABC):
    @abstractmethod
    async def exists_by(self, query_list: list[dict[str, str]]) -> bool: ...

    @abstractmethod
    async def get_by_id(self, user_id: UniqueEntityId) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def delete(self, id: UniqueEntityId) -> bool: ...
