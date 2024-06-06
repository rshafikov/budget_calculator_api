from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecordBase(BaseModel):
    amount: int


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    category_id: int
    currency_id: int
    created_at: datetime
    updated_at: datetime | None
