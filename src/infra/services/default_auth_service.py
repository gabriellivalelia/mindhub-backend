import asyncio
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import bcrypt
import jwt
from redis.asyncio import Redis

from application.dtos.patient_dto import PatientDTO
from application.dtos.psychologist_dto import PsychologistDTO
from application.services.iauth_service import IAuthService, JWTData
from domain.patient import Patient
from domain.psychologist import Psychologist
from domain.user import User
from domain.value_objects.password import Password
from infra.config.settings import Settings


class DefaultAuthService(IAuthService):
    redis_client: Redis

    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client
        self.jwt_hash_name = "activeJwtClients"
        self.token_expire_time = Settings().REFRESH_TOKEN_EXPIRE_SECONDS

    async def decode_access_token(self, token: str) -> JWTData | None:
        try:
            decoded = jwt.decode(  # type: ignore
                token, Settings().ACCESS_TOKEN_SECRET, algorithms=[Settings().ALGORITHM]
            )
            return JWTData(**decoded)
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def sign_jwt_tokens(self, user: User) -> tuple[str, str]:
        dto = None
        if isinstance(user, Patient):
            dto = PatientDTO.to_dto(user)

        elif isinstance(user, Psychologist):
            dto = PsychologistDTO.to_dto(user)

        if dto is None:
            raise ValueError("Invalid user type")

        access_token_data = JWTData(user=dto).model_dump()
        access_token_expire = datetime.now(timezone.utc) + timedelta(
            minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token_data.update({"exp": access_token_expire})
        access_token = jwt.encode(  # type: ignore
            access_token_data, Settings().ACCESS_TOKEN_SECRET, Settings().ALGORITHM
        )

        refresh_token = uuid4().hex

        return access_token, refresh_token

    async def save_authenticated_user(self, user_id: str, refresh_token: str) -> None:
        key = self._construct_key(user_id, refresh_token)
        await self.redis_client.set(key, refresh_token)
        await self.redis_client.expire(key, self.token_expire_time)

    async def de_authenticate_user(self, user_id: str) -> None:
        keys = await self.redis_client.keys(f"*{self.jwt_hash_name}.{user_id}*")  # type: ignore
        if keys:
            await self.redis_client.delete(*keys)

    async def get_tokens(self, user_id: str) -> list[str]:
        keys: list[str] = await self.redis_client.keys(  # type: ignore
            f"*{self.jwt_hash_name}.{user_id}*"
        )
        return await asyncio.gather(*[self.redis_client.get(key) for key in keys])  # type: ignore

    def _construct_key(self, user_id: str, refresh_token: str) -> str:
        return f"refresh-{refresh_token}.{self.jwt_hash_name}.{user_id}"

    async def hash_password(self, password: Password) -> Password:
        hashed = bcrypt.hashpw(password.value.encode("utf-8"), bcrypt.gensalt())
        return Password(value=hashed.decode("utf-8"), hashed=True)

    async def verify_password(
        self, password: Password, hashed_password: Password
    ) -> bool:
        return bcrypt.checkpw(
            password.value.encode("utf-8"), hashed_password.value.encode("utf-8")
        )
