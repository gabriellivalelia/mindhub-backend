from application.common.page import Page
from application.common.pageable import Pageable
from application.common.use_case import IUseCase
from application.dtos.patient_dto import PatientDTO
from application.filters.patient_filters import PatientFilters
from application.repos.ipatient_repo import IPatientRepo


class GetPatientsDTO(Pageable, PatientFilters): ...


class GetPatientsUseCase(IUseCase[GetPatientsDTO, Page[PatientDTO]]):
    patient_repo: IPatientRepo

    def __init__(
        self,
        patient_repo: IPatientRepo,
    ) -> None:
        self.patient_repo = patient_repo

    async def execute(self, dto: GetPatientsDTO) -> Page[PatientDTO]:
        pageable = Pageable(page=dto.page, size=dto.size)
        filters = PatientFilters(
            name=dto.name,
            city_id=dto.city_id,
            state_id=dto.state_id,
        )

        page = await self.patient_repo.get(pageable, filters)
        return Page(
            items=[PatientDTO.to_dto(entity) for entity in page.items],
            total=page.total,
            pageable=page.pageable,
        )
