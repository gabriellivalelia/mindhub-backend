from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.approach_dto import ApproachDTO
from application.repos.iapproach_repo import IApproachRepo
from domain.common.unique_entity_id import UniqueEntityId


class GetApproachByIdDTO(BaseModel):
    approach_id: UUID


class GetApproachByIdUseCase(IUseCase[GetApproachByIdDTO, ApproachDTO]):
    approach_repo: IApproachRepo

    def __init__(self, approach_repo: IApproachRepo) -> None:
        self.approach_repo = approach_repo

    async def execute(self, dto: GetApproachByIdDTO) -> ApproachDTO:
        approach = await self.approach_repo.get_by_id(UniqueEntityId(dto.approach_id))

        if not approach:
            raise ApplicationException("Abordagem não encontrada.")

        return ApproachDTO.to_dto(approach)
