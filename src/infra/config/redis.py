from contextlib import asynccontextmanager
from typing import AsyncGenerator

import redis.asyncio as redis

from infra.config.logger import logger
from infra.config.settings import Settings


class RedisManager:
    @classmethod
    @asynccontextmanager
    async def connect(cls) -> AsyncGenerator[redis.Redis, None]:
        client = redis.from_url(  # type: ignore
            f"redis://{Settings().REDIS_HOST}:{Settings().REDIS_PORT}?decode_responses=True"
        )
        logger.info("✅ Established connection with redis")

        try:
            yield client
        finally:
            await client.close()
