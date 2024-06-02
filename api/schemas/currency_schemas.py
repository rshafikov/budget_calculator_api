from datetime import datetime

from pydantic import BaseModel


class CurrencyBase(BaseModel):
    name: str
    symbol: str | None


class CurrencyCreate(CurrencyBase):
    pass


class Currency(CurrencyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
