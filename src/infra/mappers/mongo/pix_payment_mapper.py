from domain.common.unique_entity_id import UniqueEntityId
from domain.pix_payment import PaymentStatusEnum, PixPayment
from infra.mappers.imapper import IMapper
from infra.models.mongo.appointment_document import PixPaymentDocument


class PixPaymentMongoMapper(IMapper[PixPaymentDocument, PixPayment]):
    @staticmethod
    async def to_domain(model: PixPaymentDocument) -> PixPayment:
        return PixPayment(
            amount=model.amount,
            provider_payment_id=model.provider_payment_id,
            pix_payload=model.pix_payload,
            expires_at=model.expires_at,
            status=PaymentStatusEnum(model.status),
            id=UniqueEntityId(model.id),
        )

    @staticmethod
    async def to_model(entity: PixPayment) -> PixPaymentDocument:
        return PixPaymentDocument(
            id=entity.id.value,
            amount=entity.amount,
            provider_payment_id=entity.provider_payment_id,
            pix_payload=entity.pix_payload,
            expires_at=entity.expires_at,
            status=entity.status.value,
        )
