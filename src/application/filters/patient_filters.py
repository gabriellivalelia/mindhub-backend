from pydantic import BaseModel


class PatientFilters(BaseModel):
    name: str | None = None
    email: str | None = None
    city_id: str | None = None
    state_id: str | None = None

    class Config:
        extra = "forbid"
