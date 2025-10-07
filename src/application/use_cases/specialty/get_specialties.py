from application.common.page import Page
from application.common.pageable import Pageable
from application.common.use_case import IUseCase
from application.dtos.specialty_dto import SpecialtyDTO
from application.filters.specialty_filters import SpecialtyFilters
from application.repos.ispecialty_repo import ISpecialtyRepo


class GetSpecialtiesDTO(Pageable, SpecialtyFilters): ...


class GetSpecialtiesUseCase(IUseCase[GetSpecialtiesDTO, Page[SpecialtyDTO]]):
    specialty_repo: ISpecialtyRepo

    def __init__(self, specialty_repo: ISpecialtyRepo) -> None:
        self.specialty_repo = specialty_repo

    async def execute(self, dto: GetSpecialtiesDTO) -> Page[SpecialtyDTO]:
        pageable = Pageable(page=dto.page, size=dto.size, sort=dto.sort)
        filters = SpecialtyFilters(name=dto.name)

        page = await self.specialty_repo.get(pageable, filters)
        return Page[SpecialtyDTO](
            items=[SpecialtyDTO.to_dto(entity) for entity in page.items],
            total=page.total,
            pageable=page.pageable,
        )
