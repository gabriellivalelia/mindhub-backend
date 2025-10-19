from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from uuid import uuid4

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

    async def seed(self) -> None:
        total_states = await StateDocument.count()
        total_specialties = await SpecialtyDocument.count()
        total_approaches = await ApproachDocument.count()
        if total_states > 0 and total_specialties > 0 and total_approaches > 0:
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

        # Seed Approaches - Abordagens Psicológicas Completas
        approaches_data = [
            {
                "name": "Terapia Cognitivo-Comportamental (TCC)",
                "description": "Abordagem estruturada focada na identificação e modificação de padrões de pensamento disfuncionais e comportamentos inadequados para promover mudanças emocionais positivas",
            },
            {
                "name": "Psicanálise",
                "description": "Método de investigação psíquica baseado nas teorias freudianas que busca compreender o inconsciente através da interpretação dos sonhos, lapsos e associações livres",
            },
            {
                "name": "Psicanálise Lacaniana",
                "description": "Abordagem psicanalítica baseada nas teorias de Jacques Lacan, enfatizando a linguagem, o simbólico e a estrutura do sujeito do inconsciente",
            },
            {
                "name": "Gestalt-Terapia",
                "description": "Abordagem humanística que enfatiza a consciência do momento presente, integração de experiências e responsabilidade pessoal através do contato genuíno",
            },
            {
                "name": "Terapia Humanística",
                "description": "Abordagem centrada na pessoa que valoriza o potencial humano, a auto-realização e o crescimento pessoal através de um ambiente terapêutico empático e não-diretivo",
            },
            {
                "name": "Terapia Sistêmica Familiar",
                "description": "Abordagem que considera o indivíduo inserido em sistemas relacionais, focando nos padrões de interação familiar e nas dinâmicas interpessoais",
            },
            {
                "name": "Terapia de Casal",
                "description": "Modalidade terapêutica especializada em trabalhar conflitos conjugais, comunicação e dinâmicas relacionais entre parceiros íntimos",
            },
            {
                "name": "EMDR (Dessensibilização e Reprocessamento por Movimentos Oculares)",
                "description": "Técnica específica para tratamento de traumas que utiliza movimentos oculares bilaterais para facilitar o processamento de memórias traumáticas",
            },
            {
                "name": "Terapia Comportamental Dialética (DBT)",
                "description": "Abordagem que combina técnicas cognitivo-comportamentais com mindfulness, focada no desenvolvimento de habilidades de regulação emocional",
            },
            {
                "name": "Terapia de Aceitação e Compromisso (ACT)",
                "description": "Abordagem que utiliza mindfulness e valores pessoais para aumentar a flexibilidade psicológica e reduzir o sofrimento emocional",
            },
            {
                "name": "Mindfulness e Meditação",
                "description": "Práticas de atenção plena derivadas de tradições contemplativas, aplicadas terapeuticamente para redução do estresse e aumento da consciência",
            },
            {
                "name": "Terapia Psicodramática",
                "description": "Método terapêutico criado por Jacob Moreno que utiliza técnicas de dramatização, role-playing e expressão corporal para explorar questões psicológicas",
            },
            {
                "name": "Arteterapia",
                "description": "Uso terapêutico de expressões artísticas como pintura, desenho, escultura e outras formas criativas para facilitar a expressão e elaboração emocional",
            },
            {
                "name": "Musicoterapia",
                "description": "Utilização da música e elementos musicais como meio terapêutico para promover comunicação, expressão e bem-estar emocional",
            },
            {
                "name": "Terapia Narrativa",
                "description": "Abordagem que ajuda pessoas a re-escrever suas histórias de vida, identificando narrativas dominantes e construindo versões mais capacitadoras",
            },
            {
                "name": "Terapia Focada na Emoção (EFT)",
                "description": "Abordagem humanística-experiencial que ajuda clientes a acessar, processar e transformar emoções para promover mudanças terapêuticas",
            },
            {
                "name": "Terapia Breve Estratégica",
                "description": "Modelo terapêutico focado na resolução rápida de problemas através de intervenções estratégicas e mudanças nos padrões comportamentais",
            },
            {
                "name": "Hipnoterapia",
                "description": "Uso terapêutico do estado de transe hipnótico para acessar recursos inconscientes e promover mudanças comportamentais e emocionais",
            },
            {
                "name": "Terapia Corporal",
                "description": "Abordagens que integram corpo e mente, utilizando técnicas corporais, respiração e movimento para promover integração e cura",
            },
            {
                "name": "Análise Bioenergética",
                "description": "Método terapêutico desenvolvido por Alexander Lowen que trabalha a relação entre corpo, energia e caráter psicológico",
            },
            {
                "name": "Terapia Reichiana",
                "description": "Abordagem baseada nas teorias de Wilhelm Reich que integra trabalho corporal e análise de caráter para liberar bloqueios energéticos",
            },
            {
                "name": "Terapia Existencial",
                "description": "Abordagem filosófica que explora questões fundamentais da existência humana como liberdade, responsabilidade, morte e significado da vida",
            },
            {
                "name": "Logoterapia",
                "description": "Método criado por Viktor Frankl focado na busca de sentido e significado como motivação primária do ser humano",
            },
            {
                "name": "Terapia Transpessoal",
                "description": "Abordagem que integra dimensões espirituais e transcendentes da experiência humana ao processo terapêutico",
            },
            {
                "name": "Constelações Familiares",
                "description": "Método terapêutico desenvolvido por Bert Hellinger que trabalha dinâmicas familiares sistêmicas através de representações espaciais",
            },
            {
                "name": "Programação Neurolinguística (PNL)",
                "description": "Conjunto de técnicas que estuda a relação entre linguagem, comportamento e padrões neurológicos para promover mudanças pessoais",
            },
            {
                "name": "Terapia Cognitiva Baseada em Mindfulness (MBCT)",
                "description": "Integração de técnicas cognitivas com práticas de mindfulness para prevenção de recaídas depressivas e manejo de pensamentos ruminativos",
            },
            {
                "name": "Terapia do Esquema",
                "description": "Abordagem integrativa que combina elementos cognitivo-comportamentais, gestálticos e relacionais para tratar transtornos de personalidade",
            },
            {
                "name": "Terapia Racional Emotiva Comportamental (TREC)",
                "description": "Método criado por Albert Ellis que foca na identificação e mudança de crenças irracionais que geram sofrimento emocional",
            },
            {
                "name": "Terapia Interpessoal (TIP)",
                "description": "Abordagem estruturada que foca nos padrões de relacionamento interpessoal e sua conexão com sintomas psicológicos",
            },
        ]

        for approach_data in approaches_data:
            await ApproachDocument(
                id=uuid4(),
                name=approach_data["name"],
                description=approach_data["description"],
            ).save()
