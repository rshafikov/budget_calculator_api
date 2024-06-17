from datetime import datetime

from pydantic import BaseModel, ConfigDict

from api.schemas.category_schemas import Category, CategoryBase


class RecordBase(BaseModel):
    amount: float


class RecordResponse(RecordBase):
    category_name: str


class RecordCreate(RecordBase):
    user_id: int
    category_id: int
    currency_id: int


class Record(RecordCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None = None
    category: Category


class RecordExternal(RecordBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    category: CategoryBase
    currency_id: int
