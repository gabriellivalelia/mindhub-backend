from typing import AsyncGenerator

import redis.asyncio as redis
from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.services.iauth_service import IAuthService
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
