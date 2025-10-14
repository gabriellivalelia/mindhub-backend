from pydantic import BaseModel

from application.common.use_case import IUseCase
from application.dtos.specialty_dto import SpecialtyDTO
from application.repos.ispecialty_repo import ISpecialtyRepo
from domain.specialty import Specialty


class CreateSpecialtyDTO(BaseModel):
    name: str
    description: str


class CreateSpecialtyUseCase(IUseCase[CreateSpecialtyDTO, SpecialtyDTO]):
    specialty_repo: ISpecialtyRepo

    def __init__(self, specialty_repo: ISpecialtyRepo) -> None:
        self.specialty_repo = specialty_repo

    async def execute(self, dto: CreateSpecialtyDTO) -> SpecialtyDTO:
        specialty = Specialty(
            name=dto.name,
            description=dto.description,
            id=None,
        )

        created_specialty = await self.specialty_repo.create(specialty)
        return SpecialtyDTO.to_dto(created_specialty)
