from datetime import date
from uuid import UUID, uuid4

from beanie import Document, Link
from pydantic import EmailStr, Field
from pymongo import IndexModel

from domain.user import GenderEnum
from domain.value_objects.file_data import FileData
from infra.models.mongo.city_document import CityDocument


class UserDocument(Document):
    id: UUID = Field(default_factory=uuid4)  # type: ignore
    name: str = Field(..., description="Patient name")
    email: EmailStr = Field(..., description="Patient email")
    password_hash: str = Field(..., description="Hashed password")
    cpf: str = Field(..., description="Patient CPF", min_length=11, max_length=11)
    phone_number: str = Field(..., description="Patient phone number")
    birth_date: date = Field(..., description="Patient birth date")
    gender: GenderEnum = Field(..., description="Patient gender")
    city: Link[CityDocument] = Field(..., description="Reference to city")
    profile_picture: FileData | None = Field(
        default=None, description="Profile picture data"
    )

    class Settings:
        name = "users"
        is_root = True
        indexes = [
            IndexModel("email", unique=True),
            IndexModel("cpf", unique=True),
        ]
