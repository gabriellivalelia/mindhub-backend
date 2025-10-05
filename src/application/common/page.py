from pydantic import BaseModel, Field, computed_field

from application.common.pageable import Pageable


class Page[T](BaseModel):
    items: list[T]
    pageable: Pageable = Field(...)
    total: int = Field(..., ge=0)

    @computed_field
    @property
    def page(self) -> int:
        return self.pageable.page

    @computed_field
    @property
    def size(self) -> int:
        return self.pageable.size

    @computed_field
    @property
    def total_pages(self) -> int:
        if self.size == 0:
            return 0

        return (self.total + self.size - 1) // self.size

    @computed_field
    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @computed_field
    @property
    def has_prev(self) -> bool:
        return self.page > 1

    class Config:
        arbitrary_types_allowed = True
