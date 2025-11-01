"""Seeder para abordagens terapêuticas."""

import asyncio
from uuid import uuid4

from infra.database.seeds.data.approaches import APPROACHES
from infra.models.mongo.approach_document import ApproachDocument


async def seed_approaches() -> dict[str, ApproachDocument]:
    """
    Popula a coleção de abordagens no banco de dados.

    Returns:
        dict: Dicionário mapeando nome da abordagem para o documento criado.
    """
    print("🌱 Iniciando seed de abordagens...")

    approaches_map = {}

    for approach_data in APPROACHES:
        # Verifica se já existe
        existing = await ApproachDocument.find_one(ApproachDocument.name == approach_data["name"])

        if existing:
            print(f"  ⏭️  Abordagem '{approach_data['name']}' já existe. Pulando...")
            approaches_map[approach_data["name"]] = existing
            continue

        # Cria novo documento
        approach = ApproachDocument(
            id=uuid4(),
            name=approach_data["name"],
            description=approach_data["description"],
        )

        await approach.insert()
        approaches_map[approach_data["name"]] = approach
        print(f"  ✅ Abordagem '{approach_data['name']}' criada com sucesso!")

    print(f"✨ Seed de abordagens concluído! Total: {len(approaches_map)} abordagens.\n")
    return approaches_map


if __name__ == "__main__":
    # Para executar standalone (necessário inicializar beanie antes)
    asyncio.run(seed_approaches())
