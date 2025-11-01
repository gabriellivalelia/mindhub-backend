"""Seeder para dados geográficos (estados e cidades) usando API do IBGE."""

import asyncio

from infra.models.mongo.city_document import CityDocument
from infra.models.mongo.state_document import StateDocument
from infra.services.ibge_service import IBGEService


async def seed_geography() -> tuple[dict[str, StateDocument], dict[tuple[str, str], CityDocument]]:
    """
    Popula as coleções de estados e cidades no banco de dados usando dados do IBGE.
    Este processo é automático e busca todos os estados e municípios do Brasil.

    Returns:
        tuple: (
            dict mapeando abreviação do estado para o documento criado,
            dict mapeando (nome_cidade, sigla_estado) para o documento da cidade
        )
    """
    print("🌱 Iniciando seed de dados geográficos (IBGE)...")
    print("   📡 Buscando dados da API do IBGE...")

    ibge_service = IBGEService()
    states_map = {}
    cities_map = {}

    try:
        # Busca estados e cidades do IBGE
        state_documents, city_documents = await ibge_service.seed_brazilian_data()

        print(f"   ✅ {len(state_documents)} estados e {len(city_documents)} cidades obtidos do IBGE\n")
        print("   💾 Salvando no banco de dados...")

        # Salva os estados
        for state_doc in state_documents:
            # Verifica se já existe
            existing_state = await StateDocument.find_one(StateDocument.abbreviation == state_doc.abbreviation)

            if existing_state:
                print(f"  ⏭️  Estado '{state_doc.name}' já existe. Pulando...")
                states_map[state_doc.abbreviation] = existing_state
            else:
                await state_doc.insert()
                states_map[state_doc.abbreviation] = state_doc
                print(f"  ✅ Estado '{state_doc.name}' criado com sucesso!")

        # Salva as cidades
        cities_count = 0
        for city_doc in city_documents:
            # Busca o estado já salvo no banco
            state_abbr = next(
                (abbr for abbr, state in states_map.items() if state.id == city_doc.state.id),
                None,
            )

            if not state_abbr:
                print(f"  ⚠️  Estado não encontrado para cidade '{city_doc.name}'. Pulando...")
                continue

            # Verifica se já existe
            saved_state = states_map[state_abbr]
            existing_city = await CityDocument.find_one(
                CityDocument.name == city_doc.name,
                CityDocument.state.id == saved_state.id,  # type: ignore
            )

            if existing_city:
                cities_map[(city_doc.name, state_abbr)] = existing_city
                cities_count += 1
            else:
                # Atualiza a referência do estado para o documento salvo
                city_doc.state = saved_state  # type: ignore
                await city_doc.insert()
                cities_map[(city_doc.name, state_abbr)] = city_doc
                cities_count += 1

                # Mostra progresso a cada 100 cidades
                if cities_count % 100 == 0:
                    print(f"    💾 {cities_count} cidades salvas...")

        print(f"\n✨ Seed de geografia concluído! Total: {len(states_map)} estados e {len(cities_map)} cidades.\n")
        return states_map, cities_map

    except Exception as e:
        print(f"❌ Erro ao buscar dados do IBGE: {e}")
        raise

    finally:
        await ibge_service.close()


if __name__ == "__main__":
    # Para executar standalone (necessário inicializar beanie antes)
    asyncio.run(seed_geography())
