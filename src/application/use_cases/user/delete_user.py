from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.repos.iuser_repo import IUserRepo
from domain.common.unique_entity_id import UniqueEntityId


class DeleteUserDTO(BaseModel):
    user_id: UUID


class DeleteUserUseCase(IUseCase[DeleteUserDTO, bool]):
    user_repo: IUserRepo

    def __init__(
        self,
        user_repo: IUserRepo,
    ) -> None:
        self.user_repo = user_repo

    async def execute(self, dto: DeleteUserDTO) -> bool:
        user = await self.user_repo.get_by_id(UniqueEntityId(dto.user_id))
        if not user:
            raise ApplicationException("User not found.")

        deleted = await self.user_repo.delete(UniqueEntityId(dto.user_id))

        if not deleted:
            raise ApplicationException("Failed to delete user.")

        return deleted
