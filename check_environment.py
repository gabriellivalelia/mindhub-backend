#!/usr/bin/env python3
"""Script de verificação do ambiente MindHub Backend."""

import sys
from pathlib import Path

# Adiciona src ao path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


def check_dependencies():
    """Verifica se as dependências estão instaladas."""
    print("🔍 Verificando dependências...")

    dependencies = {
        "fastapi": "FastAPI",
        "beanie": "Beanie (MongoDB ODM)",
        "redis": "Redis",
        "bcrypt": "bcrypt",
        "pydantic": "Pydantic",
        "jwt": "PyJWT",
        "motor": "Motor (MongoDB Async)",
    }

    missing = []
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - NÃO INSTALADO")
            missing.append(name)

    if missing:
        print(f"\n❌ Dependências faltando: {', '.join(missing)}")
        print("   Execute: uv sync")
        return False

    print("✅ Todas as dependências estão instaladas!\n")
    return True


def check_env_file():
    """Verifica se o arquivo .env existe."""
    print("🔍 Verificando arquivo .env...")

    env_file = Path(__file__).parent / ".env"
    env_example = Path(__file__).parent / ".env.example"

    if env_file.exists():
        print("  ✅ Arquivo .env encontrado")
        return True
    else:
        print("  ❌ Arquivo .env NÃO encontrado")
        if env_example.exists():
            print(f"     Copie o arquivo de exemplo: cp {env_example} {env_file}")
        print()
        return False


def check_mongodb():
    """Verifica se o MongoDB está acessível."""
    print("🔍 Verificando conexão com MongoDB...")

    try:
        from motor.motor_asyncio import AsyncIOMotorClient

        from infra.config.settings import Settings

        settings = Settings()

        # Tenta conectar (com timeout curto)
        import asyncio

        async def test_connection():
            client = AsyncIOMotorClient(settings.MONGO_URI, serverSelectionTimeoutMS=3000)
            try:
                await client.admin.command("ping")
                return True
            except Exception as e:
                print(f"  ❌ Erro ao conectar: {e}")
                return False
            finally:
                client.close()

        result = asyncio.run(test_connection())

        if result:
            print(f"  ✅ MongoDB conectado em {settings.MONGO_URI}")
            print(f"  ✅ Database: {settings.MONGO_DATABASE_NAME}")
            return True
        else:
            print("  ❌ MongoDB não está acessível")
            print("     Execute: docker compose up -d")
            print()
            return False

    except Exception as e:
        print(f"  ❌ Erro ao verificar MongoDB: {e}")
        print()
        return False


def check_redis():
    """Verifica se o Redis está acessível."""
    print("🔍 Verificando conexão com Redis...")

    try:
        import redis

        from infra.config.settings import Settings

        settings = Settings()

        # Tenta conectar (com timeout curto)
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, socket_connect_timeout=3)
        r.ping()

        print(f"  ✅ Redis conectado em {settings.REDIS_HOST}:{settings.REDIS_PORT}")
        return True

    except Exception as e:
        print(f"  ❌ Redis não está acessível: {e}")
        print("     Execute: docker compose up -d")
        print()
        return False


def check_seeds():
    """Verifica se o banco de dados tem dados."""
    print("🔍 Verificando dados no banco...")

    try:
        from beanie import init_beanie
        from motor.motor_asyncio import AsyncIOMotorClient

        from infra.config.settings import Settings
        from infra.models.mongo.approach_document import ApproachDocument
        from infra.models.mongo.psychologist_document import PsychologistDocument
        from infra.models.mongo.specialty_document import SpecialtyDocument
        from infra.models.mongo.state_document import StateDocument

        settings = Settings()

        import asyncio

        async def check_data():
            client = AsyncIOMotorClient(settings.MONGO_URI)
            database = client[settings.MONGO_DATABASE_NAME]

            await init_beanie(
                database=database,
                document_models=[
                    SpecialtyDocument,
                    ApproachDocument,
                    StateDocument,
                    PsychologistDocument,
                ],
            )

            try:
                specialties_count = await SpecialtyDocument.count()
                approaches_count = await ApproachDocument.count()
                states_count = await StateDocument.count()
                psychologists_count = await PsychologistDocument.count()

                print(f"  📊 Especialidades: {specialties_count}")
                print(f"  📊 Abordagens: {approaches_count}")
                print(f"  📊 Estados: {states_count}")
                print(f"  📊 Psicólogos: {psychologists_count}")

                if specialties_count == 0 or approaches_count == 0 or states_count == 0 or psychologists_count == 0:
                    print("\n  ⚠️  Banco de dados vazio ou incompleto")
                    print("     Execute os seeds: uv run poe seed")
                    return False
                else:
                    print("  ✅ Banco de dados populado!")
                    return True

            finally:
                client.close()

        return asyncio.run(check_data())

    except Exception as e:
        print(f"  ❌ Erro ao verificar dados: {e}")
        print()
        return False


def main():
    """Função principal."""
    print("=" * 70)
    print("🏥 MINDHUB BACKEND - VERIFICAÇÃO DE AMBIENTE")
    print("=" * 70)
    print()

    checks = [
        ("Dependências", check_dependencies),
        ("Arquivo .env", check_env_file),
        ("MongoDB", check_mongodb),
        ("Redis", check_redis),
        ("Dados (Seeds)", check_seeds),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erro ao verificar {name}: {e}\n")
            results.append((name, False))

    # Resumo
    print("=" * 70)
    print("📋 RESUMO")
    print("=" * 70)

    all_passed = True
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
        if not result:
            all_passed = False

    print()

    if all_passed:
        print("🎉 Tudo pronto! O ambiente está configurado corretamente.")
        print()
        print("🚀 Para iniciar o servidor:")
        print("   uv run poe dev")
    else:
        print("⚠️  Alguns problemas foram encontrados. Corrija-os antes de continuar.")
        print()
        print("📚 Guia rápido:")
        print("   1. Instalar dependências: uv sync")
        print("   2. Configurar .env: cp .env.example .env")
        print("   3. Iniciar serviços: docker compose up -d")
        print("   4. Popular banco: uv run poe seed")

    print("=" * 70)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
