from abc import ABC

from domain.value_objects.password import Password


class IAuthService(ABC):
    async def hash_password(self, password: Password) -> Password: ...

    async def verify_password(
        self, password: Password, hashed_password: Password
    ) -> bool: ...
