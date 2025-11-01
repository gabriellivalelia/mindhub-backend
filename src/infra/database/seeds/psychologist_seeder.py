"""Seeder para psicólogos com disponibilidades dinâmicas."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

try:
    import bcrypt
except ImportError:
    bcrypt = None  # type: ignore

from infra.database.seeds.data.psychologists import PSYCHOLOGISTS
from infra.models.mongo.approach_document import ApproachDocument
from infra.models.mongo.availability_document import AvailabilityDocument
from infra.models.mongo.city_document import CityDocument
from infra.models.mongo.psychologist_document import PsychologistDocument
from infra.models.mongo.specialty_document import SpecialtyDocument


def generate_availabilities(start_date: datetime, num_days: int = 14) -> list[AvailabilityDocument]:
    """
    Gera disponibilidades para os próximos N dias.

    Args:
        start_date: Data de início (geralmente amanhã)
        num_days: Número de dias para gerar disponibilidades (padrão: 14 dias / 2 semanas)

    Returns:
        list: Lista de AvailabilityDocument
    """
    availabilities = []

    # Horários de atendimento: 8h às 18h, em intervalos de 1 hora
    working_hours = [8, 9, 10, 11, 14, 15, 16, 17, 18]

    for day_offset in range(num_days):
        current_date = start_date + timedelta(days=day_offset)

        # Pula fins de semana (sábado=5, domingo=6)
        if current_date.weekday() >= 5:
            continue

        for hour in working_hours:
            availability_datetime = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)

            availability = AvailabilityDocument(
                id=uuid4(),
                date=availability_datetime,
                available=True,
            )
            availabilities.append(availability)

    return availabilities


async def seed_psychologists(
    specialties_map: dict[str, SpecialtyDocument],
    approaches_map: dict[str, ApproachDocument],
    cities_map: dict[tuple[str, str], CityDocument],
) -> list[PsychologistDocument]:
    """
    Popula a coleção de psicólogos no banco de dados.

    Args:
        specialties_map: Mapa de especialidades (nome -> documento)
        approaches_map: Mapa de abordagens (nome -> documento)
        cities_map: Mapa de cidades ((nome, estado) -> documento)

    Returns:
        list: Lista de PsychologistDocument criados
    """
    print("🌱 Iniciando seed de psicólogos...")

    psychologists_created = []

    # Gerar disponibilidades começando de amanhã
    tomorrow = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

    for psych_data in PSYCHOLOGISTS:
        # Verifica se já existe (por email)
        existing = await PsychologistDocument.find_one(PsychologistDocument.email == psych_data["email"])

        if existing:
            print(f"  ⏭️  Psicólogo '{psych_data['name']}' já existe. Pulando...")
            psychologists_created.append(existing)
            continue

        # Hash da senha
        password_hash = bcrypt.hashpw(psych_data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Busca cidade
        city_key = (psych_data["city"], psych_data["state"])
        city = cities_map.get(city_key)

        if not city:
            print(f"  ❌ Cidade '{psych_data['city']}/{psych_data['state']}' não encontrada. Pulando psicólogo...")
            continue

        # Busca especialidades
        specialties = []
        for specialty_name in psych_data["specialties"]:
            specialty = specialties_map.get(specialty_name)
            if specialty:
                specialties.append(specialty)

        # Busca abordagens
        approaches = []
        for approach_name in psych_data["approaches"]:
            approach = approaches_map.get(approach_name)
            if approach:
                approaches.append(approach)

        # Gera disponibilidades para as próximas 2 semanas
        availabilities = generate_availabilities(tomorrow, num_days=14)

        # Cria o psicólogo
        psychologist = PsychologistDocument(
            id=uuid4(),
            name=psych_data["name"],
            email=psych_data["email"],
            password_hash=password_hash,
            cpf=psych_data["cpf"],
            crp=psych_data["crp"],
            phone_number=psych_data["phone_number"],
            birth_date=psych_data["birth_date"],
            gender=psych_data["gender"],
            city=city,
            description=psych_data.get("description"),
            value_per_appointment=psych_data["value_per_appointment"],
            specialties=specialties,
            approaches=approaches,
            audiences=psych_data["audiences"],
            availabilities=availabilities,
            profile_picture=None,
        )

        await psychologist.insert()
        psychologists_created.append(psychologist)
        print(f"  ✅ Psicólogo '{psych_data['name']}' criado com {len(availabilities)} disponibilidades!")

    print(f"✨ Seed de psicólogos concluído! Total: {len(psychologists_created)} psicólogos.\n")
    return psychologists_created


if __name__ == "__main__":
    # Para executar standalone (necessário inicializar beanie e carregar dependências antes)
    print("Este seeder deve ser executado através do run_seeds.py")
