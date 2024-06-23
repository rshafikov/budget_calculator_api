import enum
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from api.schemas.category_schemas import Category, CategoryBase
from api.schemas.currency_schemas import Currency
from api.schemas.record_schemas import Record, RecordExternal


class Role(enum.Enum):
    ADMIN: str = "admin"
    USER: str = "user"

    def __hash__(self):
        return hash(str(self.value))

    def __str__(self):
        return str(self.value)


class UserBase(BaseModel):
    telegram_id: str
    name: str | None = None
    lastname: str | None = None


class UserCreate(UserBase):
    password: str


class AdminCreate(UserCreate):
    role: Role


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    password: str
    role: Role
    created_at: datetime
    updated_at: datetime

    records: list[Record | None]
    categories: list[Category | None]
    currency: Currency


class UserSecure(UserBase):
    model_config = ConfigDict(from_attributes=True)

    currency: Currency
    records: list[RecordExternal | None]
    categories: list[CategoryBase | None]
