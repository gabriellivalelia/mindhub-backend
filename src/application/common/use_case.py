from abc import ABC, abstractmethod


class IUseCase[IRequest, IResponse](ABC):
    @abstractmethod
    async def execute(self, dto: IRequest) -> IResponse: ...
