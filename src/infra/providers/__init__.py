from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from .base_provider import BaseProvider
from .psychologist_provider import PsychologistProvider

container = make_async_container(
    FastapiProvider(),
    BaseProvider(),
    PsychologistProvider(),
)
