from domain.common.entity import Entity
from domain.common.guard import Guard
from domain.common.unique_entity_id import UniqueEntityId


class State(Entity):
    def __init__(
        self, name: str, abbreviation: str, id: UniqueEntityId | None = None
    ) -> None:
        Guard.against_undefined_bulk(
            [
                {"argument": name, "argument_name": "name"},
                {"argument": abbreviation, "argument_name": "abbreviation"},
            ]
        )

        super().__init__(id)
        self._name = name
        self._abbreviation = abbreviation

    @property
    def name(self) -> str:
        return self._name

    @property
    def abbreviation(self) -> str:
        return self._abbreviation
