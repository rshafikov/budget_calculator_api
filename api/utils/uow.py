from abc import ABC, abstractmethod

from api.db.database import async_session_maker
from api.repositories.user_repository import UserRepository


class IUnitOfWork(ABC):
    user: UserRepository

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, *args):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self._session_factory = async_session_maker
        self.session = None

    async def __aenter__(self):
        self.session = self._session_factory()
        self.user = UserRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
