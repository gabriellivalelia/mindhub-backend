from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from beanie import init_beanie  # type: ignore
from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import AsyncClientSession

from infra.config.logger import logger
from infra.config.settings import Settings
from infra.models.mongo.appointment_document import (
    AppointmentDocument,
    PixPaymentDocument,
)
from infra.models.mongo.approach_document import ApproachDocument
from infra.models.mongo.availability_document import AvailabilityDocument
from infra.models.mongo.city_document import CityDocument
from infra.models.mongo.content_document import ContentDocument
from infra.models.mongo.patient_document import PatientDocument
from infra.models.mongo.psychologist_document import PsychologistDocument
from infra.models.mongo.specialty_document import SpecialtyDocument
from infra.models.mongo.state_document import StateDocument


class MongoManager:
    _client: AsyncMongoClient[Any]

    def __init__(self, client: AsyncMongoClient[Any]) -> None:
        self._client = client

    @classmethod
    @asynccontextmanager
    async def connect(cls) -> AsyncGenerator[MongoManager, None]:
        settings = Settings()
        client = AsyncMongoClient[Any](settings.MONGO_URI, uuidRepresentation="standard")

        await init_beanie(
            database=client[settings.MONGO_DATABASE_NAME],
            document_models=[
                StateDocument,
                CityDocument,
                PatientDocument,
                PsychologistDocument,
                SpecialtyDocument,
                ApproachDocument,
                AvailabilityDocument,
                PixPaymentDocument,
                AppointmentDocument,
                ContentDocument,
            ],
        )

        logger.info("✅ Established connection with MongoDB and initialized Beanie")

        manager = cls(client)
        await manager.seed()

        try:
            yield manager
        finally:
            await client.close()

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncClientSession, None]:
        assert self._client is not None

        async with self._client.start_session() as session:
            async with await session.start_transaction():
                yield session
