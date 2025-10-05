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
from infra.models.mongo.availability_document import AvailabilityDocument
from infra.models.mongo.city_document import CityDocument
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
        client = AsyncMongoClient[Any](
            settings.MONGO_URI, uuidRepresentation="standard"
        )

        await init_beanie(
            database=client[settings.MONGO_DATABASE_NAME],
            document_models=[
                StateDocument,
                CityDocument,
                PatientDocument,
                PsychologistDocument,
                SpecialtyDocument,
                AvailabilityDocument,
                PixPaymentDocument,
                AppointmentDocument,
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

    async def seed(self) -> None:
        total_states = await StateDocument.count()
        total_specialties = await SpecialtyDocument.count()
        if total_states > 0 and total_specialties > 0:
            return

        # # Seed States and Cities using IBGE API
        # from infra.services.ibge_service import IBGEService

        # ibge_service = IBGEService()
        # try:
        #     state_documents, city_documents = await ibge_service.seed_brazilian_data()

        #     # Save states first
        #     for state_doc in state_documents:
        #         await state_doc.save()

        #     # Then save cities
        #     for city_doc in city_documents:
        #         await city_doc.save()

        # except Exception as e:
        #     logger.warning(f"Failed to seed data from IBGE API: {e}")
        #     logger.info("Falling back to basic seed data...")

        #     # Fallback to basic states and cities if IBGE fails
        #     ba = StateDocument(name="Bahia", abbreviation="BA")
        #     await ba.save()

        #     mg = StateDocument(name="Minas Gerais", abbreviation="MG")
        #     await mg.save()

        #     sp = StateDocument(name="São Paulo", abbreviation="SP")
        #     await sp.save()

        #     await CityDocument(name="Salvador", state=ba).save()  # type: ignore
        #     await CityDocument(name="Belo Horizonte", state=mg).save()  # type: ignore
        #     await CityDocument(name="São Paulo", state=sp).save()  # type: ignore
        # finally:
        #     await ibge_service.close()

        # # Seed Specialties
        # specialties_data = [
        #     {
        #         "name": "Ansiedade",
        #         "description": "Tratamento especializado para transtornos de ansiedade",
        #     },
        #     {
        #         "name": "Depressão",
        #         "description": "Acompanhamento psicológico para quadros depressivos",
        #     },
        #     {
        #         "name": "Terapia de Casal",
        #         "description": "Orientação e terapia para relacionamentos",
        #     },
        #     {
        #         "name": "Psicologia Infantil",
        #         "description": "Atendimento psicológico especializado para crianças",
        #     },
        #     {
        #         "name": "Transtornos Alimentares",
        #         "description": "Tratamento para anorexia, bulimia e outros transtornos alimentares",
        #     },
        #     {
        #         "name": "Terapia Cognitivo-Comportamental",
        #         "description": "Abordagem TCC para diversos transtornos",
        #     },
        #     {
        #         "name": "Síndrome do Pânico",
        #         "description": "Tratamento especializado para ataques de pânico",
        #     },
        #     {
        #         "name": "Luto e Perdas",
        #         "description": "Acompanhamento psicológico em processos de luto",
        #     },
        #     {
        #         "name": "Estresse Pós-Traumático",
        #         "description": "Tratamento para transtorno de estresse pós-traumático",
        #     },
        #     {
        #         "name": "Orientação Profissional",
        #         "description": "Orientação vocacional e de carreira",
        #     },
        # ]

        # for specialty_data in specialties_data:
        #     await SpecialtyDocument(
        #         id=uuid4(),
        #         name=specialty_data["name"],
        #         description=specialty_data["description"],
        #     ).save()
