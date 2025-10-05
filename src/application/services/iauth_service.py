from abc import ABC, abstractmethod

from pydantic import BaseModel

from application.dtos.user_dto import UserDTO
from domain.user import User
from domain.value_objects.password import Password


class JWTData(BaseModel):
    user: UserDTO


class IAuthService(ABC):
    @abstractmethod
    async def hash_password(self, password: Password) -> Password: ...

    @abstractmethod
    async def verify_password(
        self, password: Password, hashed_password: Password
    ) -> bool: ...

    @abstractmethod
    def sign_jwt_tokens(self, user: User) -> tuple[str, str]: ...

    @abstractmethod
    async def decode_access_token(self, token: str) -> JWTData | None: ...

    @abstractmethod
    async def save_authenticated_user(
        self, user_id: str, refresh_token: str
    ) -> None: ...

    @abstractmethod
    async def de_authenticate_user(self, user_id: str) -> None: ...

    @abstractmethod
    async def get_tokens(self, user_id: str) -> list[str]: ...

    @abstractmethod
    def _construct_key(self, user_id: str, refresh_token: str) -> str: ...
