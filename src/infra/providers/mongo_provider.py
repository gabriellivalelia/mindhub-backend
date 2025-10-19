from __future__ import annotations

from typing import AsyncGenerator

from dishka import (
    Provider,
    Scope,
    provide,  # type: ignore
)
from pymongo.asynchronous.client_session import AsyncClientSession

from application.repos.iappointment_repo import IAppointmentRepo
from application.repos.iapproach_repo import IApproachRepo
from application.repos.icity_repo import ICityRepo
from application.repos.icontent_repo import IContentRepo
from application.repos.ipatient_repo import IPatientRepo
from application.repos.ipsychologist_repo import IPsychologistRepo
from application.repos.ispecialty_repo import ISpecialtyRepo
from application.repos.istate_repo import IStateRepo
from application.repos.iuser_repo import IUserRepo
from infra.config.mongo_db_manager import MongoManager
from infra.repos.mongo.appointment_repo import MongoAppointmentRepo
from infra.repos.mongo.approach_repo import MongoApproachRepo
from infra.repos.mongo.city_repo import MongoCityRepo
from infra.repos.mongo.content_repo import MongoContentRepo
from infra.repos.mongo.patient_repo import MongoPatientRepo
from infra.repos.mongo.psychologist_repo import MongoPsychologistRepo
from infra.repos.mongo.specialty_repo import MongoSpecialtyRepo
from infra.repos.mongo.state_repo import MongoStateRepo
from infra.repos.mongo.user_repo import MongoUserRepo


class MongoDBProvider(Provider):
    @provide(scope=Scope.APP)
    async def MongoDBManager(self) -> AsyncGenerator[MongoManager]:
        async with MongoManager.connect() as db_manager:
            yield db_manager

    @provide(scope=Scope.REQUEST)
    async def MongoDBSession(
        self, db_manager: MongoManager
    ) -> AsyncGenerator[AsyncClientSession]:
        async with db_manager.get_session() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def UserRepo(self, session: AsyncClientSession) -> IUserRepo:
        return MongoUserRepo(session)

    @provide(scope=Scope.REQUEST)
    def PatientRepo(self, session: AsyncClientSession) -> IPatientRepo:
        return MongoPatientRepo(session)

    @provide(scope=Scope.REQUEST)
    def CityRepo(self, session: AsyncClientSession) -> ICityRepo:
        return MongoCityRepo(session)

    @provide(scope=Scope.REQUEST)
    def StateRepo(self, session: AsyncClientSession) -> IStateRepo:
        return MongoStateRepo(session)

    @provide(scope=Scope.REQUEST)
    def PsychologistRepo(self, session: AsyncClientSession) -> IPsychologistRepo:
        return MongoPsychologistRepo(session)

    @provide(scope=Scope.REQUEST)
    def SpecialtyRepo(self, session: AsyncClientSession) -> ISpecialtyRepo:
        return MongoSpecialtyRepo(session)

    @provide(scope=Scope.REQUEST)
    def ApproachRepo(self, session: AsyncClientSession) -> IApproachRepo:
        return MongoApproachRepo(session)

    @provide(scope=Scope.REQUEST)
    def ContentRepo(self, session: AsyncClientSession) -> IContentRepo:
        return MongoContentRepo(session)

    @provide(scope=Scope.REQUEST)
    def AppointmentRepo(self, session: AsyncClientSession) -> IAppointmentRepo:
        return MongoAppointmentRepo(session)
