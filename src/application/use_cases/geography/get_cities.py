from application.common.page import Page
from application.common.pageable import Pageable
from application.common.use_case import IUseCase
from application.dtos.city_dto import CityDTO
from application.filters.city_filters import CityFilters
from application.repos.icity_repo import ICityRepo


class GetCitiesDTO(Pageable, CityFilters): ...


class GetCitiesUseCase(IUseCase[GetCitiesDTO, Page[CityDTO]]):
    city_repo: ICityRepo

    def __init__(
        self,
        city_repo: ICityRepo,
    ) -> None:
        self.city_repo = city_repo

    async def execute(self, dto: GetCitiesDTO) -> Page[CityDTO]:
        pageable = Pageable(page=dto.page, size=dto.size)
        filters = CityFilters(
            name=dto.name,
            state_id=dto.state_id,
        )

        page = await self.city_repo.get(pageable, filters)
        return Page[CityDTO](
            items=[CityDTO.to_dto(entity) for entity in page.items],
            total=page.total,
            pageable=page.pageable,
        )
