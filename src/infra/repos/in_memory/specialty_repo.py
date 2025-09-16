from uuid import UUID

from application.repos.ispecialty_repo import ISpecialtyRepo
from domain.common.unique_entity_id import UniqueEntityId
from domain.specialty import Specialty


class InMemorySpecialtyRepo(ISpecialtyRepo):
    items: list[Specialty] = [
        Specialty(
            id=UniqueEntityId(UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")),
            name="Ansiedade",
            description="Ansiedade",
        )
    ]

    def __init__(self) -> None: ...

    async def save(self, entity: Specialty) -> Specialty:
        InMemorySpecialtyRepo.items.append(entity)
        return entity

    async def get_by_ids(self, ids: list[UniqueEntityId]) -> list[Specialty]:
        return [item for item in InMemorySpecialtyRepo.items if item.id in ids]

    async def get_by_id(self, id: UniqueEntityId) -> Specialty | None:
        return next(
            (item for item in InMemorySpecialtyRepo.items if item.id == id), None
        )
