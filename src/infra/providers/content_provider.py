from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)

from application.repos.icontent_repo import IContentRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from application.use_cases.content.create_content import CreateContentUseCase
from application.use_cases.content.delete_content import DeleteContentUseCase
from application.use_cases.content.get_content_by_id import GetContentByIdUseCase
from application.use_cases.content.get_contents import GetContentsUseCase
from application.use_cases.content.update_content import UpdateContentUseCase


class ContentProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def CreateContentUseCaseInstance(
        self,
        content_repo: IContentRepo,
        psychologist_repo: IPsychologistRepo,
    ) -> CreateContentUseCase:
        return CreateContentUseCase(content_repo, psychologist_repo)

    @provide(scope=Scope.REQUEST)
    def GetContentsUseCaseInstance(
        self, content_repo: IContentRepo
    ) -> GetContentsUseCase:
        return GetContentsUseCase(content_repo)

    @provide(scope=Scope.REQUEST)
    def GetContentByIdUseCaseInstance(
        self, content_repo: IContentRepo
    ) -> GetContentByIdUseCase:
        return GetContentByIdUseCase(content_repo)

    @provide(scope=Scope.REQUEST)
    def UpdateContentUseCaseInstance(
        self, content_repo: IContentRepo
    ) -> UpdateContentUseCase:
        return UpdateContentUseCase(content_repo)

    @provide(scope=Scope.REQUEST)
    def DeleteContentUseCaseInstance(
        self, content_repo: IContentRepo
    ) -> DeleteContentUseCase:
        return DeleteContentUseCase(content_repo)
