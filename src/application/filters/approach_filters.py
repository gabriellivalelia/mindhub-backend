from pydantic import BaseModel


class ApproachFilters(BaseModel):
    name: str | None = None
