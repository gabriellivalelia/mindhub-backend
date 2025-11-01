from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.content_dto import ContentDTO
from application.repos.icontent_repo import IContentRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.common.unique_entity_id import UniqueEntityId


class GetContentByIdDTO(BaseModel):
    content_id: UUID


class GetContentByIdUseCase(IUseCase[GetContentByIdDTO, ContentDTO]):
    content_repo: IContentRepo
    psychologist_repo: IPsychologistRepo

    def __init__(self, content_repo: IContentRepo, psychologist_repo: IPsychologistRepo) -> None:
        self.content_repo = content_repo
        self.psychologist_repo = psychologist_repo

    async def execute(self, dto: GetContentByIdDTO) -> ContentDTO:
        content = await self.content_repo.get_by_id(UniqueEntityId(dto.content_id))
        if not content:
            raise ApplicationException("Conteúdo não encontrado")

        # Buscar nome do autor
        author = await self.psychologist_repo.get_by_id(content.author_id)
        author_name = author.name if author else None

        return ContentDTO.to_dto(content, author_name)
