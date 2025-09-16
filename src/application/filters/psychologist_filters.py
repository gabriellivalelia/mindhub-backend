from pydantic import BaseModel


class PsychologistFilters(BaseModel):
    name: str | None = None
    city_id: str | None = None
    state_id: str | None = None
    specialty_ids: set[str] | None = None
    approaches: set[str] | None = None
    audiences: set[str] | None = None
    min_price: float | None = None
    max_price: float | None = None

    class Config:
        extra = "forbid"
