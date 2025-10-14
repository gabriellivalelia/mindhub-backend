from uuid import UUID

from pydantic import BaseModel

from application.common.exception import ApplicationException
from application.common.use_case import IUseCase
from application.dtos.patient_dto import PatientDTO
from application.repos.ipatient_repo import IPatientRepo
from domain.common.unique_entity_id import UniqueEntityId


class GetPatientByIdDTO(BaseModel):
    patient_id: UUID


class GetPatientByIdUseCase(IUseCase[GetPatientByIdDTO, PatientDTO]):
    patient_repo: IPatientRepo

    def __init__(self, patient_repo: IPatientRepo) -> None:
        self.patient_repo = patient_repo

    async def execute(self, dto: GetPatientByIdDTO) -> PatientDTO:
        patient = await self.patient_repo.get_by_id(UniqueEntityId(dto.patient_id))

        if not patient:
            raise ApplicationException("Patient not found.")

        return PatientDTO.to_dto(patient)
