from application.common.page import Page
from application.common.pageable import Pageable
from application.common.use_case import IUseCase
from application.dtos.approach_dto import ApproachDTO
from application.filters.approach_filters import ApproachFilters
from application.repos.iapproach_repo import IApproachRepo


class GetApproachesDTO(Pageable, ApproachFilters): ...


class GetApproachesUseCase(IUseCase[GetApproachesDTO, Page[ApproachDTO]]):
    approach_repo: IApproachRepo

    def __init__(self, approach_repo: IApproachRepo) -> None:
        self.approach_repo = approach_repo

    async def execute(self, dto: GetApproachesDTO) -> Page[ApproachDTO]:
        pageable = Pageable(page=dto.page, size=dto.size, sort=dto.sort)
        filters = ApproachFilters(name=dto.name)

        page = await self.approach_repo.get(pageable, filters)
        return Page[ApproachDTO](
            items=[ApproachDTO.to_dto(entity) for entity in page.items],
            total=page.total,
            pageable=page.pageable,
        )
