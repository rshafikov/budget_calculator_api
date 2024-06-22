from datetime import datetime

from pydantic import BaseModel, ConfigDict

from api.schemas.category_schemas import Category, CategoryBase
from api.schemas.currency_schemas import Currency


class RecordBase(BaseModel):
    amount: float


class RecordRequest(RecordBase):
    category_name: str
    currency: Currency | None = None


class RecordCreate(RecordBase):
    user_id: int
    category_id: int
    currency: Currency


class Record(RecordCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime | None = None
    category: Category
    currency: Currency


class RecordExternal(RecordBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    category: CategoryBase
    currency: Currency
