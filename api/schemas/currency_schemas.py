from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CurrencyBase(BaseModel):
    name: str
    symbol: str | None


class CurrencyCreate(CurrencyBase):
    pass


class Currency(CurrencyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime