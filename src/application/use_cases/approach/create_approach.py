from pydantic import BaseModel

from application.common.use_case import IUseCase
from application.dtos.approach_dto import ApproachDTO
from application.repos.iapproach_repo import IApproachRepo
from domain.approach import Approach


class CreateApproachDTO(BaseModel):
    name: str
    description: str


class CreateApproachUseCase(IUseCase[CreateApproachDTO, ApproachDTO]):
    approach_repo: IApproachRepo

    def __init__(self, approach_repo: IApproachRepo) -> None:
        self.approach_repo = approach_repo

    async def execute(self, dto: CreateApproachDTO) -> ApproachDTO:
        approach = Approach(
            name=dto.name,
            description=dto.description,
        )

        created_approach = await self.approach_repo.create(approach)
        return ApproachDTO.to_dto(created_approach)
