from contextlib import asynccontextmanager
from typing import AsyncGenerator, TypedDict

from fastapi import FastAPI


class LifeSpan(TypedDict): ...


class MindHubApp:
    __app: FastAPI

    def __init__(self):
        self.__app = FastAPI(
            title="MindHub",
            version="1.0.0",
            docs_url="/docs",
            summary="API do MindHub",
            lifespan=self.__lifespan,
        )

    @asynccontextmanager
    async def __lifespan(self, app: FastAPI) -> AsyncGenerator[LifeSpan, None]:
        yield {}

    @property
    def app(self) -> FastAPI:
        return self.__app
