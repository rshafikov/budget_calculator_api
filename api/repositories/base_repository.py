from abc import ABC, abstractmethod

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def count(self):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        query = insert(self.model).values(**data).returning(self.model)
        r = await self.session.execute(query)

        return r.scalar_one()

    async def get_one(self, **kwargs):
        r = await self.session.execute(select(self.model).filter_by(**kwargs))
        return r.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 100):
        r = await self.session.execute(
            select(self.model).offset(offset).limit(limit)
        )
        return r.scalars().all()

    async def count(self):
        query = select(func.count()).select_from(self.model)
        r = await self.session.execute(query)
        return r.scalar_one()
