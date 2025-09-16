from abc import ABC, abstractmethod


class IMapper[E, M](ABC):
    @staticmethod
    @abstractmethod
    async def to_domain(model: E) -> M: ...

    @staticmethod
    @abstractmethod
    async def to_model(entity: M) -> E: ...
