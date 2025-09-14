from domain.common.entity import Entity
from domain.common.guard import Guard
from domain.common.unique_entity_id import UniqueEntityId
from domain.state import State


class City(Entity):
    def __init__(
        self,
        state: State,
        name: str,
        abbreviation: str,
        id: UniqueEntityId | None = None,
    ) -> None:
        Guard.against_undefined_bulk(
            [
                {"argument": state, "argument_name": "state"},
                {"argument": name, "argument_name": "name"},
                {"argument": abbreviation, "argument_name": "abbreviation"},
            ]
        )

        super().__init__(id)

        self._name = name
        self._abbreviation = abbreviation
        self._state = state

    @property
    def name(self) -> str:
        return self._name

    @property
    def abbreviation(self) -> str:
        return self._abbreviation

    @property
    def state(self) -> State:
        return self._state
