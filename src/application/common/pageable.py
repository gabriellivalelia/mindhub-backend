from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, field_validator

from domain.common.guard import Guard, GuardException


class SORT_DIRECTION(Enum):
    ASC = "asc"
    DESC = "desc"


PAGE_DEFAULT = 1
SIZE_DEFAULT = 10


class Pageable(BaseModel):
    page: int = Field(PAGE_DEFAULT, ge=1)
    size: int = Field(SIZE_DEFAULT, ge=1)
    sort: list[tuple[str, SORT_DIRECTION]] | None = None

    model_config = {"extra": "forbid"}

    @field_validator("sort", mode="before")
    @classmethod
    def _normalize_sort(
        cls, v: list[tuple[str, str]] | tuple[tuple[str, str], ...] | None
    ) -> list[tuple[str, SORT_DIRECTION]] | None:
        if v is None:
            return None

        normalized: list[tuple[str, SORT_DIRECTION]] = []
        for item in v:
            if not isinstance(item, (list, tuple)) or len(item) != 2:  # type: ignore
                raise GuardException(
                    "each sort item must be a (field, direction) tuple"
                )

            field_name, direction = item
            direction = str(direction).lower()
            Guard.is_one_of_enum(direction, SORT_DIRECTION, f"sort(f{field_name})")

            normalized.append((str(field_name), SORT_DIRECTION(direction)))

        return normalized

    def offset(self) -> int:
        return (self.page - 1) * self.size

    def limit(self) -> int:
        return self.size

    def next(self) -> Pageable:
        return Pageable(page=self.page + 1, size=self.size, sort=self.sort)

    def previous(self) -> Pageable:
        prev_page = self.page - 1 if self.page > 1 else 1
        return Pageable(page=prev_page, size=self.size, sort=self.sort)
