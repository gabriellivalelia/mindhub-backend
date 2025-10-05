from typing import AsyncGenerator

import redis.asyncio as redis
from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer

from application.services.iauth_service import IAuthService, JWTData
from application.services.ifile_service import IFileService
from infra.config.redis import RedisManager
from infra.services.default_auth_service import DefaultAuthService
from infra.services.local_file_service import LocalFileService


class BaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def RedisClient(self) -> AsyncGenerator[redis.Redis]:
        async with RedisManager().connect() as client:
            yield client

    @provide(scope=Scope.APP)
    def FileServiceImpl(self) -> IFileService:
        return LocalFileService()

    @provide(scope=Scope.APP)
    def AuthServiceImpl(self, redis_client: redis.Redis) -> IAuthService:
        return DefaultAuthService(redis_client)

    @provide(scope=Scope.REQUEST)
    async def Auth(self, request: Request, auth_service: IAuthService) -> JWTData:
        credentials = await HTTPBearer(auto_error=True)(request)
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme",
            )

        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme",
            )

        decoded = await auth_service.decode_access_token(credentials.credentials)
        if decoded is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token",
            )

        tokens = await auth_service.get_tokens(str(decoded.user.id))
        if len(tokens) == 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Auth token not found. User is probably not logged in. Please login again",
            )

        return decoded
