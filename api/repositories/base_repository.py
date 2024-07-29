import logging
from abc import ABC, abstractmethod

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from api.db.models import BaseModel

logger = logging.getLogger(__name__)


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

    @abstractmethod
    async def delete_one(self):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, instance_id, data: dict):
        raise NotImplementedError


class Repository(AbstractRepository):
    model: BaseModel | None = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        q = insert(self.model).values(**data).returning(self.model)
        try:
            r = await self.session.execute(q)
            return r.scalar_one()
        except IntegrityError as err:
            logger.error('Unable to create instance %r: %s', data, err)
            raise err

    async def get_one(self, **kwargs):
        q = select(self.model).filter_by(**kwargs)
        r = await self.session.execute(q)
        return r.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 100, **kwargs):
        q = select(self.model).offset(offset).limit(limit).filter_by(**kwargs)
        r = await self.session.execute(q)
        return r.scalars().all()

    async def count(self, **kwargs):
        q = select(func.count()).select_from(self.model).filter_by(**kwargs)
        return await self.session.scalar(q)

    async def update_one(self, instance_id, data: dict):
        try:
            q = update(
                self.model
            ).where(self.model.id == instance_id
                    ).values(**data).returning(self.model)
            result = await self.session.execute(q)
            return result.scalar_one()
        except IntegrityError as err:
            logger.error(
                'Unable to update instance %r with %r: %s',
                instance_id, data, err
            )
            raise err

    async def delete_one(self, instance=None, **kwargs):
        try:
            if instance:
                return await self.session.delete(instance)

            q = delete(self.model).filter_by(**kwargs)
            await self.session.execute(q)

        except IntegrityError as err:
            logger.error(
                'Unable to delete instance with criteria %r: %s',
                kwargs, err
            )
            raise err
