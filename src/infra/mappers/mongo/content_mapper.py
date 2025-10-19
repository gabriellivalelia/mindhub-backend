from domain.common.unique_entity_id import UniqueEntityId
from domain.content import Content
from infra.models.mongo.content_document import ContentDocument


class ContentMongoMapper:
    @staticmethod
    async def to_domain(model: ContentDocument) -> Content:
        if not model:
            return None

        return Content(
            title=model.title,
            body=model.body,
            author_id=UniqueEntityId(model.author_id),
            created_at=model.created_at,
            id=UniqueEntityId(model.id),
        )

    @staticmethod
    async def to_model(entity: Content) -> ContentDocument:
        return ContentDocument(
            id=entity.id.value,
            title=entity.title,
            body=entity.body,
            author_id=entity.author_id.value,
            created_at=entity.created_at,
        )
