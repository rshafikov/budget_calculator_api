import enum
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from api.schemas.category_schemas import Category
from api.schemas.record_schemas import Record


class Role(enum.Enum):
    ADMIN: str = "admin"
    USER: str = "user"


class UserBase(BaseModel):
    telegram_id: str
    name: str | None = None
    lastname: str | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    password: str
    role: Role
    created_at: datetime
    updated_at: datetime

    records: list[Record | None]
    categories: list[Category | None]


class UserSecure(UserBase):
    model_config = ConfigDict(from_attributes=True)

    records: list[Record | None]
    categories: list[Category | None]
