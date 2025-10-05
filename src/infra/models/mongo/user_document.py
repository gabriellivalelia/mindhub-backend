from uuid import UUID

from beanie import Document, Link
from pydantic import EmailStr
from pymongo import IndexModel

from domain.user import GenderEnum
from domain.value_objects.file_data import FileData
from infra.models.mongo.city_document import CityDocument


class UserDocument(Document):
    id: UUID
    name: str
    email: EmailStr
    password_hash: str
    cpf: str
    phone_number: str
    birth_date: str
    gender: GenderEnum
    city: Link[CityDocument]
    profile_picture: FileData | None = None

    class Settings:
        name = "users"
        is_root = True
        indexes = [
            IndexModel("email", unique=True),
            IndexModel("cpf", unique=True),
        ]
