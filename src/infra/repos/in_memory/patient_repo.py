from datetime import datetime

from application.common.page import Page
from application.common.pageable import Pageable
from application.filters.patient_filters import PatientFilters
from application.repos.ipatient_repo import IPatientRepo
from domain.appointment import Appointment
from domain.common.unique_entity_id import UniqueEntityId
from domain.patient import Patient


class InMemoryPatientRepo(IPatientRepo):
    items: list[Patient] = []

    def __init__(self) -> None: ...

    async def create(self, entity: Patient) -> Patient:
        InMemoryPatientRepo.items.append(entity)
        return entity

    async def get(
        self, pageable: Pageable, filters: PatientFilters | None = None
    ) -> Page[Patient]:
        items = InMemoryPatientRepo.items
        if filters:
            if filters.name:
                items = [p for p in items if filters.name.lower() in p.name.lower()]
            if filters.city_id:
                items = [p for p in items if str(p.city.id) == str(filters.city_id)]

        start = pageable.offset()
        end = start + pageable.size
        page_items = items[start:end]

        return Page(
            items=page_items,
            total=len(InMemoryPatientRepo.items),
            pageable=pageable,
        )

    async def get_by_id(self, id: UniqueEntityId) -> Patient | None:
        return next((item for item in InMemoryPatientRepo.items if item.id == id), None)

    async def schedule_appointment(
        self, entity: Patient, date: datetime, psychologist_id: UniqueEntityId
    ) -> Appointment | None:
        appointment = entity.schedule_appointment(date, psychologist_id)
        if appointment:
            await self.create(entity)
        return appointment
