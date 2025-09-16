from pydantic import HttpUrl

from domain.common.value_object import ValueObject


class FileData(ValueObject):
    key: str
    src: HttpUrl | str
    size: int
    filename: str
    content_type: str
