# pyright: reportUnusedFunction=false

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, TypedDict

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

from application.common.exception import ApplicationException
from domain.common.exception import DomainException
from domain.common.guard import GuardException
from infra.config.settings import Settings
from infra.providers import container
from infra.routers.patient_router import router as patient_router
from infra.routers.psychologist_router import router as psychologist_router


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

        setup_dishka(container=container, app=self.__app)

        self._set_middlewares()

        self._set_routers()

        self._set_exception_handlers()

    @asynccontextmanager
    async def __lifespan(self, app: FastAPI) -> AsyncGenerator[LifeSpan, None]:
        yield {}

        app.state.dishka_container.close()

    def _set_middlewares(self) -> None:
        self.__app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _set_routers(self) -> None:
        self.__app.include_router(psychologist_router)
        self.__app.include_router(patient_router)

        if Settings().ENV == "development":
            # Disponibiliza os arquivos salvos na pasta "/temp"
            os.makedirs(Settings().FILES_PATH, exist_ok=True)
            self.__app.mount(
                "/files", StaticFiles(directory=Settings().FILES_PATH), name="files"
            )

    def _set_exception_handlers(self) -> None:
        @self.__app.exception_handler(RequestValidationError)
        async def validation_exception_handler(
            request: Request, exc: RequestValidationError
        ):
            errors = []
            for err in exc.errors():
                loc = err.get("loc", [])
                msg = err.get("msg", "")
                err_type = err.get("type", "")
                errors.append(  # type: ignore
                    {
                        "field": ".".join(str(x) for x in loc),
                        "message": msg,
                        "error_type": err_type,
                    }
                )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Bad request",
                    "errors": errors,
                },
            )

        @self.__app.exception_handler(GuardException)
        async def guard_exception_handler(request: Request, exc: GuardException):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Bad request",
                    "errors": str(exc),
                },
            )

        @self.__app.exception_handler(DomainException)
        async def domain_exception_handler(request: Request, exc: DomainException):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Bad request",
                    "errors": str(exc),
                },
            )

        @self.__app.exception_handler(ApplicationException)
        async def application_exception_handler(
            request: Request, exc: ApplicationException
        ):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Bad request",
                    "errors": str(exc),
                },
            )

        @self.__app.exception_handler(ValidationError)
        async def pydantic_validation_exception_handler(
            request: Request, exc: ValidationError
        ):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": "Bad request",
                    "errors": exc.errors(),
                },
            )

        @self.__app.exception_handler(Exception)
        async def internal_exception_handler(request: Request, exc: Exception):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "message": "Internal server error",
                    "errors": str(exc),
                },
            )

    @property
    def app(self) -> FastAPI:
        return self.__app
