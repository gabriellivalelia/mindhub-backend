from application.common.page import Page
from application.common.pageable import Pageable
from application.common.use_case import IUseCase
from application.dtos.psychologist_dto import PsychologistDTO
from application.filters.psychologist_filters import PsychologistFilters
from application.repos.ipsychologist_repo import IPsychologistRepo


class GetPsychologistsDTO(Pageable, PsychologistFilters): ...


class GetPsychologistsUseCase(IUseCase[GetPsychologistsDTO, Page[PsychologistDTO]]):
    psychologist_repo: IPsychologistRepo

    def __init__(
        self,
        psychologist_repo: IPsychologistRepo,
    ) -> None:
        self.psychologist_repo = psychologist_repo

    async def execute(self, dto: GetPsychologistsDTO) -> Page[PsychologistDTO]:
        pageable = Pageable(page=dto.page, size=dto.size)
        filters = PsychologistFilters(
            name=dto.name,
            city_id=dto.city_id,
            state_id=dto.state_id,
            specialty_ids=dto.specialty_ids,
            approaches=dto.approaches,
            audiences=dto.audiences,
            min_price=dto.min_price,
            max_price=dto.max_price,
        )
        page = await self.psychologist_repo.get(pageable, filters)
        return Page(
            items=[PsychologistDTO.to_dto(entity) for entity in page.items],
            total=page.total,
            pageable=page.pageable,
        )
