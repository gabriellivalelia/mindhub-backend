from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from infra.providers.patient_provider import PatientProvider

from .base_provider import BaseProvider
from .psychologist_provider import PsychologistProvider

container = make_async_container(
    FastapiProvider(), BaseProvider(), PsychologistProvider(), PatientProvider()
)
