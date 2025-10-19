from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.content_dto import ContentDTO
from application.repos.icontent_repo import IContentRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from domain.common.unique_entity_id import UniqueEntityId
from domain.content import Content


class CreateContentDTO(BaseModel):
    title: str
    body: str
    author_id: UUID


class CreateContentUseCase(IUseCase[CreateContentDTO, ContentDTO]):
    content_repo: IContentRepo
    psychologist_repo: IPsychologistRepo

    def __init__(
        self,
        content_repo: IContentRepo,
        psychologist_repo: IPsychologistRepo,
    ) -> None:
        self.content_repo = content_repo
        self.psychologist_repo = psychologist_repo

    async def execute(self, dto: CreateContentDTO) -> ContentDTO:
        # Verifica se o autor é um psicólogo
        psychologist = await self.psychologist_repo.get_by_id(
            UniqueEntityId(dto.author_id)
        )
        if not psychologist:
            raise ApplicationException("Only psychologists can create content")

        content = Content(
            title=dto.title,
            body=dto.body,
            author_id=UniqueEntityId(dto.author_id),
        )

        created_content = await self.content_repo.create(content)
        return ContentDTO.to_dto(created_content)
