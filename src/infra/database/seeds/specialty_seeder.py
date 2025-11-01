"""Seeder para especialidades."""

import asyncio
from uuid import uuid4

from infra.database.seeds.data.specialties import SPECIALTIES
from infra.models.mongo.specialty_document import SpecialtyDocument


async def seed_specialties() -> dict[str, SpecialtyDocument]:
    """
    Popula a coleção de especialidades no banco de dados.

    Returns:
        dict: Dicionário mapeando nome da especialidade para o documento criado.
    """
    print("🌱 Iniciando seed de especialidades...")

    specialties_map = {}

    for specialty_data in SPECIALTIES:
        # Verifica se já existe
        existing = await SpecialtyDocument.find_one(SpecialtyDocument.name == specialty_data["name"])

        if existing:
            print(f"  ⏭️  Especialidade '{specialty_data['name']}' já existe. Pulando...")
            specialties_map[specialty_data["name"]] = existing
            continue

        # Cria novo documento
        specialty = SpecialtyDocument(
            id=uuid4(),
            name=specialty_data["name"],
            description=specialty_data["description"],
        )

        await specialty.insert()
        specialties_map[specialty_data["name"]] = specialty
        print(f"  ✅ Especialidade '{specialty_data['name']}' criada com sucesso!")

    print(f"✨ Seed de especialidades concluído! Total: {len(specialties_map)} especialidades.\n")
    return specialties_map


if __name__ == "__main__":
    # Para executar standalone (necessário inicializar beanie antes)
    asyncio.run(seed_specialties())
