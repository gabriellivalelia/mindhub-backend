from uuid import UUID

from application.common.use_case import IUseCase
from application.dtos.patient_dto import PatientDTO
from application.dtos.psychologist_dto import PsychologistDTO
from application.dtos.user_dto import UserDTO
from application.repos.iuser_repo import IUserRepo
from domain.common.unique_entity_id import UniqueEntityId
from domain.patient import Patient
from domain.psychologist import Psychologist


class MeUseCase(IUseCase[UUID, UserDTO | None]):
    user_repo: IUserRepo

    def __init__(self, user_repo: IUserRepo) -> None:
        self.user_repo = user_repo

    async def execute(self, dto: UUID) -> UserDTO | None:
        found_user = await self.user_repo.get_by_id(UniqueEntityId(dto))

        if isinstance(found_user, Patient):
            return PatientDTO.to_dto(found_user)
        elif isinstance(found_user, Psychologist):
            return PsychologistDTO.to_dto(found_user)

        return None
