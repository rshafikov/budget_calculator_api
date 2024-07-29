from datetime import datetime
from typing import List

from sqlalchemy import Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from api.schemas.currency_schemas import Currency
from api.schemas.user_schemas import Role


class BaseModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"{self.__tablename__}:(id={self.id})"


class UserModel(BaseModel):
    __tablename__ = "users"

    name: Mapped[str | None]
    lastname: Mapped[str | None]
    telegram_id: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(Enum(Role), default=Role.USER)

    records: Mapped[List["RecordModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    categories: Mapped[List["CategoryModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    currency: Mapped[Currency] = mapped_column(
        Enum(Currency), nullable=False, default=Currency.RUB
    )


class RecordModel(BaseModel):
    __tablename__ = "records"

    amount: Mapped[int]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(
        back_populates="records", lazy="selectin")

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["CategoryModel"] = relationship(
        back_populates="records", lazy="selectin"
    )

    currency: Mapped[Currency] = mapped_column(Enum(Currency), nullable=False)


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str]
    symbol: Mapped[str | None]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(back_populates="categories")

    records: Mapped[List["RecordModel"]] = relationship(
        back_populates="category"
    )
    hidden: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (
        UniqueConstraint("name", "user_id", name="_name_user_uc"),
    )


class CurrencyModel(BaseModel):
    __tablename__ = "currencies"

    name: Mapped[str]
    symbol: Mapped[str | None]
