"""Use case for getting contents with pagination and filters."""

from application.common.page import Page
from application.common.pageable import Pageable
from application.common.use_case import IUseCase
from application.dtos.content_dto import ContentDTO
from application.filters.content_filters import ContentFilters
from application.repos.icontent_repo import IContentRepo


class GetContentsDTO(Pageable, ContentFilters):
    """DTO for get contents request."""

    ...


class GetContentsUseCase(IUseCase[GetContentsDTO, Page[ContentDTO]]):
    """Use case for retrieving a paginated list of contents."""

    content_repo: IContentRepo

    def __init__(self, content_repo: IContentRepo) -> None:
        self.content_repo = content_repo

    async def execute(self, dto: GetContentsDTO) -> Page[ContentDTO]:
        pageable = Pageable(page=dto.page, size=dto.size, sort=dto.sort)
        filters = ContentFilters(title=dto.title, author_id=dto.author_id)

        page = await self.content_repo.get(pageable, filters)
        return Page[ContentDTO](
            items=[ContentDTO.to_dto(entity) for entity in page.items],
            total=page.total,
            pageable=page.pageable,
        )
