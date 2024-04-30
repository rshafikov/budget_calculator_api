from typing import Optional, List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.core.db.models import BaseModel, TimeStampMixin


class UserModel(BaseModel, TimeStampMixin):
    __tablename__ = 'users'

    name: Mapped[Optional[str]]
    lastname: Mapped[Optional[str]]
    telegram_id: Mapped[int] = mapped_column(unique=True)
    password: Mapped[str]

    records: Mapped[List['RecordModel']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )


class RecordModel(BaseModel, TimeStampMixin):
    __tablename__ = 'records'

    # id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['UserModel'] = relationship(back_populates='records')

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped['CategoryModel'] = relationship(back_populates='records')

    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id'))


class CategoryModel(BaseModel, TimeStampMixin):
    __tablename__ = 'categories'

    # id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    symbol: Mapped[Optional[str]]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['UserModel'] = relationship(back_populates='categories')

    records: Mapped[List['RecordModel']] = relationship(
        back_populates='category', cascade='all, delete-orphan'
    )

    __table_args__ = (UniqueConstraint('name', 'user_id', name='_name_user_uc'),)


class CurrencyModel(BaseModel):
    __tablename__ = 'currencies'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    symbol: Mapped[Optional[str]]
