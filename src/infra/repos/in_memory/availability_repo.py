from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.availability_filters import AvailabilityFilters
from application.repos.iavailability_repo import IAvailabilityRepo
from domain.availability import Availability
from domain.common.unique_entity_id import UniqueEntityId


class InMemoryAvailabilityRepo(IAvailabilityRepo):
    items: list[Availability] = []

    def __init__(self) -> None: ...

    async def create(self, entity: Availability) -> Availability:
        InMemoryAvailabilityRepo.items.append(entity)
        return entity

    async def get(
        self,
        pageable: Pageable,
        filters: AvailabilityFilters | None = None,
    ) -> Page[Availability]:
        items = InMemoryAvailabilityRepo.items

        if filters:
            if filters.available is not None:
                items = [a for a in items if a.available == filters.available]
            if filters.date:
                items = [a for a in items if a.date.date() == filters.date.date()]

        start = pageable.offset()
        end = start + pageable.size
        page_items = items[start:end]

        return Page(
            items=page_items,
            pageable=pageable,
            total=len(InMemoryAvailabilityRepo.items),
        )

    async def get_by_id(self, id: UniqueEntityId) -> Availability | None:
        return next(
            (item for item in InMemoryAvailabilityRepo.items if item.id == id),
            None,
        )
