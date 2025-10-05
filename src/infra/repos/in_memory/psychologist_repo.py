from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.psychologist_filters import PsychologistFilters
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.common.unique_entity_id import UniqueEntityId
from domain.psychologist import Psychologist


class InMemoryPsychologistRepo(IPsychologistRepo):
    items: list[Psychologist] = []

    def __init__(self) -> None: ...

    async def exists_by_crp(self, crp: str) -> bool:
        return any(item.crp.value == crp for item in InMemoryPsychologistRepo.items)

    async def create(self, entity: Psychologist) -> Psychologist:
        InMemoryPsychologistRepo.items.append(entity)
        return entity

    async def update(self, entity: Psychologist) -> Psychologist:
        for i, item in enumerate(InMemoryPsychologistRepo.items):
            if item.id == entity.id:
                InMemoryPsychologistRepo.items[i] = entity
                return entity
        return entity

    async def get(
        self,
        pageable: Pageable,
        filters: PsychologistFilters | None = None,
    ) -> Page[Psychologist]:
        items = InMemoryPsychologistRepo.items
        if filters:
            if filters.name:
                items = [p for p in items if filters.name.lower() in p.name.lower()]
            if filters.city_id:
                items = [p for p in items if str(p.city.id) == str(filters.city_id)]
            if filters.specialty_ids:
                items = [
                    p
                    for p in items
                    if any(str(s.id) in filters.specialty_ids for s in p.specialties)
                ]
            if filters.approaches and len(filters.approaches) > 0:
                items = [
                    p
                    for p in items
                    if any(a.value in filters.approaches for a in p.approaches)
                ]
            if filters.audiences and len(filters.audiences) > 0:
                items = [
                    p
                    for p in items
                    if any(a.value in filters.audiences for a in p.audiences)
                ]
            if filters.min_price is not None:
                items = [
                    p for p in items if p.value_per_appointment >= filters.min_price
                ]
            if filters.max_price is not None:
                items = [
                    p for p in items if p.value_per_appointment <= filters.max_price
                ]

        start = pageable.offset()
        end = start + pageable.size
        page_items = items[start:end]

        return Page(
            items=page_items,
            pageable=pageable,
            total=len(InMemoryPsychologistRepo.items),
        )

    async def get_by_id(self, id: UniqueEntityId) -> Psychologist | None:
        return next(
            (item for item in InMemoryPsychologistRepo.items if item.id == id),
            None,
        )

    async def add_availabilities(
        self,
        entity: Psychologist,
        availability_ids: list[UniqueEntityId],
    ) -> None:
        # Buscar as availabilities pelo ID no repositório de availabilities
        from infra.repos.in_memory.availability_repo import InMemoryAvailabilityRepo

        availabilities_to_add = []
        for availability_id in availability_ids:
            availability = next(
                (
                    item
                    for item in InMemoryAvailabilityRepo.items
                    if item.id == availability_id
                ),
                None,
            )
            if availability:
                availabilities_to_add.append(availability)

        # Encontrar o psicólogo na lista e atualizar suas availabilities
        for i, psychologist in enumerate(InMemoryPsychologistRepo.items):
            if psychologist.id == entity.id:
                psychologist.add_availabilities(availabilities_to_add)
                InMemoryPsychologistRepo.items[i] = psychologist
                break
