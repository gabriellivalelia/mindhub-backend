from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.content_dto import ContentDTO
from application.repos.icontent_repo import IContentRepo
from domain.common.unique_entity_id import UniqueEntityId


class UpdateContentDTO(BaseModel):
    content_id: UUID
    title: str
    body: str
    requesting_user_id: UUID


class UpdateContentUseCase(IUseCase[UpdateContentDTO, ContentDTO]):
    content_repo: IContentRepo

    def __init__(self, content_repo: IContentRepo) -> None:
        self.content_repo = content_repo

    async def execute(self, dto: UpdateContentDTO) -> ContentDTO:
        content = await self.content_repo.get_by_id(UniqueEntityId(dto.content_id))
        if not content:
            raise ApplicationException("Conteúdo não encontrado")

        # Verifica se o usuário é o autor
        if content.author_id.value != dto.requesting_user_id:
            raise ApplicationException("Apenas o autor pode atualizar este conteúdo")

        content.update(title=dto.title, body=dto.body)

        updated_content = await self.content_repo.update(content)
        return ContentDTO.to_dto(updated_content)
