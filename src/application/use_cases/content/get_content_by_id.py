from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.content_dto import ContentDTO
from application.repos.icontent_repo import IContentRepo
from domain.common.unique_entity_id import UniqueEntityId


class GetContentByIdDTO(BaseModel):
    content_id: UUID


class GetContentByIdUseCase(IUseCase[GetContentByIdDTO, ContentDTO]):
    content_repo: IContentRepo

    def __init__(self, content_repo: IContentRepo) -> None:
        self.content_repo = content_repo

    async def execute(self, dto: GetContentByIdDTO) -> ContentDTO:
        content = await self.content_repo.get_by_id(UniqueEntityId(dto.content_id))
        if not content:
            raise ApplicationException("Content not found")

        return ContentDTO.to_dto(content)
