"""Use case for getting contents with pagination and filters."""

from application.common.page import Page
from application.common.pageable import Pageable
from application.common.use_case import IUseCase
from application.dtos.content_dto import ContentDTO
from application.filters.content_filters import ContentFilters
from application.repos.icontent_repo import IContentRepo
from application.repos.ipsychologist_repo import IPsychologistRepo


class GetContentsDTO(Pageable, ContentFilters):
    """DTO for get contents request."""

    ...


class GetContentsUseCase(IUseCase[GetContentsDTO, Page[ContentDTO]]):
    """Use case for retrieving a paginated list of contents."""

    content_repo: IContentRepo
    psychologist_repo: IPsychologistRepo

    def __init__(self, content_repo: IContentRepo, psychologist_repo: IPsychologistRepo) -> None:
        self.content_repo = content_repo
        self.psychologist_repo = psychologist_repo

    async def execute(self, dto: GetContentsDTO) -> Page[ContentDTO]:
        pageable = Pageable(page=dto.page, size=dto.size, sort=dto.sort)
        filters = ContentFilters(title=dto.title, author_id=dto.author_id)

        page = await self.content_repo.get(pageable, filters)

        # Buscar nomes dos autores
        content_dtos = []
        for entity in page.items:
            author = await self.psychologist_repo.get_by_id(entity.author_id)
            author_name = author.name if author else None
            content_dtos.append(ContentDTO.to_dto(entity, author_name))

        return Page[ContentDTO](
            items=content_dtos,
            total=page.total,
            pageable=page.pageable,
        )
