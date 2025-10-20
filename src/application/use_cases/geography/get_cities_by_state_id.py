from uuid import UUID

from application.common.use_case import IUseCase
from application.dtos.city_dto import CityDTO
from application.repos.icity_repo import ICityRepo
from domain.common.unique_entity_id import UniqueEntityId


class GetCitiesByStateIdUseCase(IUseCase[UUID, list[CityDTO]]):
    city_repo: ICityRepo

    def __init__(
        self,
        city_repo: ICityRepo,
    ) -> None:
        self.city_repo = city_repo

    async def execute(self, state_id: UUID) -> list[CityDTO]:
        docs = await self.city_repo.get_all_by_state_id(UniqueEntityId(state_id))
        return [CityDTO.to_dto(doc) for doc in docs]
