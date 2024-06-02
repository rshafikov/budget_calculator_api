from datetime import datetime

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    symbol: str | None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True
