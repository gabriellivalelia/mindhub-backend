from domain.appointment import Appointment, AppointmentStatusEnum
from domain.common.unique_entity_id import UniqueEntityId
from infra.mappers.imapper import IMapper
from infra.mappers.mongo.pix_payment_mapper import PixPaymentMongoMapper
from infra.models.mongo.appointment_document import AppointmentDocument


class AppointmentMongoMapper(IMapper[AppointmentDocument, Appointment]):
    @staticmethod
    async def to_domain(model: AppointmentDocument) -> Appointment:
        pix_payment = await PixPaymentMongoMapper.to_domain(model.pix_payment)  # type: ignore

        return Appointment(
            date=model.date,
            patient_id=UniqueEntityId(model.patient_id),
            psychologist_id=UniqueEntityId(model.psychologist_id),
            value=model.value,
            pix_payment=pix_payment,
            duration_min=model.duration_min,
            status=AppointmentStatusEnum(model.status),
            availability_id=UniqueEntityId(model.availability_id) if model.availability_id else None,
            id=UniqueEntityId(model.id),
        )

    @staticmethod
    async def to_model(entity: Appointment) -> AppointmentDocument:
        pix_payment_doc = await PixPaymentMongoMapper.to_model(entity.pix_payment)

        return AppointmentDocument(
            id=entity.id.value,
            date=entity.date,
            patient_id=entity.patient_id.value,
            psychologist_id=entity.psychologist_id.value,
            value=entity.value,
            pix_payment=pix_payment_doc,  # type: ignore
            duration_min=entity.duration_min,
            status=entity.status.value,
            availability_id=entity.availability_id.value if entity.availability_id else None,
        )
