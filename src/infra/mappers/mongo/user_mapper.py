from domain.patient import Patient
from domain.user import User
from infra.mappers.imapper import IMapper
from infra.mappers.mongo.patient_mapper import PatientMongoMapper
from infra.models.mongo.patient_document import PatientDocument
from infra.models.mongo.user_document import UserDocument


class UserMongoMapper(IMapper[UserDocument, User]):
    @staticmethod
    async def to_domain(model: UserDocument) -> User:
        if isinstance(model, PatientDocument):
            return await PatientMongoMapper.to_domain(model)

        # if isinstance(model, PsychologistDocument):
        #     return await PsychologistMongoMapper.to_domain(model)

        raise ValueError("Invalid model type")

    @staticmethod
    async def to_model(entity: User) -> UserDocument:
        if isinstance(entity, Patient):
            return await PatientMongoMapper.to_model(entity)

        raise ValueError("Invalid entity type")
