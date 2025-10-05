from abc import ABC, abstractmethod

from domain.common.unique_entity_id import UniqueEntityId
from domain.user import User


class IUserRepo(ABC):
    @abstractmethod
    async def exists_by_email_or_cpf(
        self, email: str | None = None, cpf: str | None = None
    ) -> bool: ...

    @abstractmethod
    async def get_by_id(self, user_id: UniqueEntityId) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...
