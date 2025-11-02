"""Script principal para executar todos os seeds do banco de dados."""

import asyncio
import sys
from pathlib import Path

# Adiciona o diretório src ao path para imports
src_path = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(src_path))

# ruff: noqa: E402
from beanie import init_beanie  # noqa: E402
from pymongo import AsyncMongoClient  # noqa: E402

from infra.config.settings import Settings  # noqa: E402
from infra.database.seeds.approach_seeder import seed_approaches  # noqa: E402
from infra.database.seeds.geography_seeder import seed_geography  # noqa: E402
from infra.database.seeds.psychologist_seeder import seed_psychologists  # noqa: E402
from infra.database.seeds.specialty_seeder import seed_specialties  # noqa: E402
from infra.models.mongo.appointment_document import AppointmentDocument, PixPaymentDocument  # noqa: E402
from infra.models.mongo.approach_document import ApproachDocument  # noqa: E402
from infra.models.mongo.availability_document import AvailabilityDocument  # noqa: E402
from infra.models.mongo.city_document import CityDocument  # noqa: E402
from infra.models.mongo.content_document import ContentDocument  # noqa: E402
from infra.models.mongo.patient_document import PatientDocument  # noqa: E402
from infra.models.mongo.psychologist_document import PsychologistDocument  # noqa: E402
from infra.models.mongo.specialty_document import SpecialtyDocument  # noqa: E402
from infra.models.mongo.state_document import StateDocument  # noqa: E402
from infra.models.mongo.user_document import UserDocument  # noqa: E402


async def init_database():
    """Inicializa a conexão com o banco de dados e o Beanie."""
    settings = Settings()

    # Conecta ao MongoDB
    client = AsyncMongoClient(settings.MONGODB_URL, uuidRepresentation="standard")
    database = client[settings.DATABASE_NAME]

    # Inicializa o Beanie com todos os modelos
    await init_beanie(
        database=database,
        document_models=[
            UserDocument,
            PatientDocument,
            PsychologistDocument,
            SpecialtyDocument,
            ApproachDocument,
            StateDocument,
            CityDocument,
            AvailabilityDocument,
            AppointmentDocument,
            PixPaymentDocument,
            ContentDocument,
        ],
    )

    print("✅ Conexão com o banco de dados estabelecida!\n")
    return client


async def run_all_seeds():
    """Executa todos os seeders na ordem correta."""
    print("=" * 60)
    print("🚀 INICIANDO SEEDS DO MINDHUB")
    print("=" * 60)
    print()
    print("⚠️  IMPORTANTE:")
    print("   • A primeira execução pode levar alguns minutos")
    print("   • Serão buscados ~5.570 municípios do IBGE")
    print("   • Requer conexão com a internet")
    print()

    client = None
    try:
        # Inicializa banco
        client = await init_database()

        # 1. Seeds de referência (não dependem de nada)
        specialties_map = await seed_specialties()
        approaches_map = await seed_approaches()
        states_map, cities_map = await seed_geography()

        # 2. Seeds que dependem dos anteriores
        psychologists = await seed_psychologists(specialties_map, approaches_map, cities_map)

        # Resumo final
        print("=" * 60)
        print("✨ SEEDS CONCLUÍDOS COM SUCESSO!")
        print("=" * 60)
        print("📊 Resumo:")
        print(f"  • {len(specialties_map)} especialidades")
        print(f"  • {len(approaches_map)} abordagens")
        print(f"  • {len(states_map)} estados")
        print(f"  • {len(cities_map)} municípios")
        print(f"  • {len(psychologists)} psicólogos")
        print()
        print("🎉 Banco de dados populado e pronto para uso!")
        print("=" * 60)

    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERRO AO EXECUTAR SEEDS")
        print("=" * 60)
        print(f"Erro: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    finally:
        # Fecha conexão com o banco
        if client:
            client.close()
            print("\n🔌 Conexão com o banco de dados fechada.")


def main():
    """Função principal."""
    asyncio.run(run_all_seeds())


if __name__ == "__main__":
    main()
