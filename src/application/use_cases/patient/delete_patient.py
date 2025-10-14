from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.repos.ipatient_repo import IPatientRepo
from domain.common.unique_entity_id import UniqueEntityId


class DeletePatientDTO(BaseModel):
    patient_id: UUID
    requesting_user_id: UUID  # ID of the authenticated user making the request


class DeletePatientUseCase(IUseCase[DeletePatientDTO, bool]):
    patient_repo: IPatientRepo

    def __init__(
        self,
        patient_repo: IPatientRepo,
    ) -> None:
        self.patient_repo = patient_repo

    async def execute(self, dto: DeletePatientDTO) -> bool:
        # Verify that the patient exists and belongs to the authenticated user
        patient = await self.patient_repo.get_by_id(UniqueEntityId(dto.patient_id))
        if not patient:
            raise ApplicationException("Patient not found.")

        # Verify that the authenticated user is the owner of the patient account
        if patient.id.value != dto.requesting_user_id:
            raise ApplicationException("You can only delete your own account.")

        # Delete the patient
        deleted = await self.patient_repo.delete(UniqueEntityId(dto.patient_id))

        if not deleted:
            raise ApplicationException("Failed to delete patient.")

        return deleted
