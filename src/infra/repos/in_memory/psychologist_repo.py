from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.psychologist_filters import PsychologistFilters
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.common.unique_entity_id import UniqueEntityId
from domain.psychologist import Psychologist


class InMemoryPsychologistRepo(IPsychologistRepo):
    items: list[Psychologist] = []

    def __init__(self) -> None: ...

    async def save(self, entity: Psychologist) -> Psychologist:
        InMemoryPsychologistRepo.items.append(entity)
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

        start = pageable.offset()
        end = start + pageable.size
        page_items = items[start:end]

        return Page(
            items=page_items,
            total=len(InMemoryPsychologistRepo.items),
            pageable=pageable,
        )

    async def get_by_id(self, id: UniqueEntityId) -> Psychologist | None:
        return next(
            (item for item in InMemoryPsychologistRepo.items if item.id == id),
            None,
        )
