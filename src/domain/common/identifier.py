from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class Identifier[T](ABC):
    value: T

    def __str__(self) -> str:
        return str(self.value)
