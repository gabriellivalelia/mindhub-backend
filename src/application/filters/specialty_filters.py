from pydantic import BaseModel


class SpecialtyFilters(BaseModel):
    name: str | None = None
