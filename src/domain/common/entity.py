from typing import Annotated
from fastapi import Query


class Entity:
    id: Annotated[int, Query(gt=0)]

    def __init__(self, id: int):
        self.id = id
