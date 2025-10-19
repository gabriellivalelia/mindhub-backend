from datetime import datetime

from domain.common.entity import Entity
from domain.common.exception import DomainException
from domain.common.guard import Guard
from domain.common.unique_entity_id import UniqueEntityId


class Content(Entity):
    def __init__(
        self,
        title: str,
        body: str,
        author_id: UniqueEntityId,
        created_at: datetime | None = None,
        id: UniqueEntityId | None = None,
    ) -> None:
        Guard.against_undefined_bulk(
            [
                {"argument": title, "argument_name": "title"},
                {"argument": body, "argument_name": "body"},
                {"argument": author_id, "argument_name": "author_id"},
            ]
        )

        super().__init__(id)

        if not title.strip():
            raise DomainException("Title cannot be empty")

        self._title = title
        self._body = body
        self._author_id = author_id
        self._created_at = created_at or datetime.now()

    @property
    def title(self) -> str:
        return self._title

    @property
    def body(self) -> str:
        return self._body

    @property
    def author_id(self) -> UniqueEntityId:
        return self._author_id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def update(self, title: str | None = None, body: str | None = None) -> None:
        if title is not None:
            if not title.strip():
                raise DomainException("Title cannot be empty")
            self._title = title

        if body is not None:
            self._body = body
