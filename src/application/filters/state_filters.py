from pydantic import BaseModel


class StateFilters(BaseModel):
    name: str | None = None
