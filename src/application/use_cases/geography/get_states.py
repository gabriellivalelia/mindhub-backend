from application.common.page import Page
from application.common.pageable import Pageable
from application.common.use_case import IUseCase
from application.dtos.state_dto import StateDTO
from application.filters.state_filters import StateFilters
from application.repos.istate_repo import IStateRepo


class GetStatesDTO(Pageable, StateFilters): ...


class GetStatesUseCase(IUseCase[GetStatesDTO, Page[StateDTO]]):
    state_repo: IStateRepo

    def __init__(
        self,
        state_repo: IStateRepo,
    ) -> None:
        self.state_repo = state_repo

    async def execute(self, dto: GetStatesDTO) -> Page[StateDTO]:
        pageable = Pageable(page=dto.page, size=dto.size)
        filters = StateFilters(
            name=dto.name,
        )

        page = await self.state_repo.get(pageable, filters)
        return Page[StateDTO](
            items=[StateDTO.to_dto(entity) for entity in page.items],
            total=page.total,
            pageable=page.pageable,
        )
