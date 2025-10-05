from uuid import UUID

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.city_filters import CityFilters
from application.repos.icity_repo import ICityRepo
from domain.city import City
from domain.common.unique_entity_id import UniqueEntityId
from domain.state import State


class InMemoryCityRepo(ICityRepo):
    items: list[City] = [
        City(
            id=UniqueEntityId(UUID("fc3b6acc-57df-43b5-af57-5ff78608e71a")),
            state=State(name="São Paulo", abbreviation="SP"),
            name="São Paulo",
        ),
        City(
            id=UniqueEntityId(UUID("fc3b6acc-57df-43b5-af57-5ff78608e71a")),
            state=State(name="Bahia", abbreviation="BA"),
            name="Salvador",
        ),
        City(
            id=UniqueEntityId(UUID("f0678630-c3c0-4d8c-8a2a-1e7555c15cb5")),
            state=State(name="Espírito Santo", abbreviation="ES"),
            name="Muniz Freire",
        ),
    ]

    async def get(
        self,
        pageable: Pageable,
        filters: CityFilters | None = None,
    ) -> Page[City]:
        start = pageable.offset()
        end = start + pageable.size
        page_items = InMemoryCityRepo.items[start:end]

        return Page(
            items=page_items,
            total=len(InMemoryCityRepo.items),
            pageable=pageable,
        )

    async def get_by_id(self, id: UniqueEntityId) -> City | None:
        return next((item for item in InMemoryCityRepo.items if item.id == id), None)
