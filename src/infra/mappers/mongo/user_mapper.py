from application.common.exception import ApplicationException
from domain.patient import Patient
from domain.psychologist import Psychologist
from domain.user import User
from infra.mappers.imapper import IMapper
from infra.mappers.mongo.patient_mapper import PatientMongoMapper
from infra.mappers.mongo.psychologist_mapper import PsychologistMongoMapper
from infra.models.mongo.patient_document import PatientDocument
from infra.models.mongo.psychologist_document import PsychologistDocument
from infra.models.mongo.user_document import UserDocument


class UserMongoMapper(IMapper[UserDocument, User]):
    @staticmethod
    async def to_domain(model: UserDocument) -> User:
        if isinstance(model, PatientDocument):
            return await PatientMongoMapper.to_domain(model)

        if isinstance(model, PsychologistDocument):
            return await PsychologistMongoMapper.to_domain(model)

        raise ApplicationException("Invalid model type")

    @staticmethod
    async def to_model(entity: User) -> UserDocument:
        if isinstance(entity, Patient):
            return await PatientMongoMapper.to_model(entity)

        if isinstance(entity, Psychologist):
            return await PsychologistMongoMapper.to_model(entity)

        raise ApplicationException("Invalid entity type")
