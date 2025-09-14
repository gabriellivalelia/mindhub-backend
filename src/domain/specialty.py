from domain.common.entity import Entity
from domain.common.guard import Guard
from domain.common.unique_entity_id import UniqueEntityId


class Specialty(Entity):
    def __init__(self, name: str, description: str, id: UniqueEntityId | None) -> None:
        Guard.against_empty_str_bulk(
            [
                {"argument": name, "argument_name": "name"},
                {"argument": description, "argument_name": "description"},
            ]
        )

        super().__init__(id)

        self._name = name
        self._description = description

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description
