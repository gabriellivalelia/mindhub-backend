from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.repos.icontent_repo import IContentRepo
from domain.common.unique_entity_id import UniqueEntityId


class DeleteContentDTO(BaseModel):
    content_id: UUID
    requesting_user_id: UUID


class DeleteContentUseCase(IUseCase[DeleteContentDTO, bool]):
    content_repo: IContentRepo

    def __init__(self, content_repo: IContentRepo) -> None:
        self.content_repo = content_repo

    async def execute(self, dto: DeleteContentDTO) -> bool:
        content = await self.content_repo.get_by_id(UniqueEntityId(dto.content_id))
        if not content:
            raise ApplicationException("Conteúdo não encontrado")

        # Verifica se o usuário é o autor
        if content.author_id.value != dto.requesting_user_id:
            raise ApplicationException("Apenas o autor pode deletar este conteúdo")

        return await self.content_repo.delete(UniqueEntityId(dto.content_id))
