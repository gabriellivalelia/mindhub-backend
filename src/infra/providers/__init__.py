from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from infra.providers.approach_provider import ApproachProvider
from infra.providers.base_provider import BaseProvider
from infra.providers.geography_provider import GeographyProvider
from infra.providers.patient_provider import PatientProvider
from infra.providers.session_provider import SessionProvider
from infra.providers.specialty_provider import SpecialtyProvider
from infra.providers.user_provider import UserProvider

from .mongo_provider import MongoDBProvider
from .psychologist_provider import PsychologistProvider

container = make_async_container(
    FastapiProvider(),
    BaseProvider(),
    SessionProvider(),
    MongoDBProvider(),
    PsychologistProvider(),
    PatientProvider(),
    GeographyProvider(),
    ApproachProvider(),
    SpecialtyProvider(),
    UserProvider(),
)
