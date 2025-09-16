import bcrypt

from application.services.iauth_service import IAuthService
from domain.value_objects.password import Password


class BcryptAuthService(IAuthService):
    async def hash_password(self, password: Password) -> Password:
        hashed = bcrypt.hashpw(password.value.encode("utf-8"), bcrypt.gensalt())
        return Password(value=hashed.decode("utf-8"), hashed=True)

    async def verify_password(
        self, password: Password, hashed_password: Password
    ) -> bool:
        return bcrypt.checkpw(
            password.value.encode("utf-8"), hashed_password.value.encode("utf-8")
        )
