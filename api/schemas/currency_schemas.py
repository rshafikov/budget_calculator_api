import enum
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Currency(str, enum.Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'


class CurrencyBase(BaseModel):
    name: str
    symbol: str | None = None


class CurrencyDB(CurrencyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
