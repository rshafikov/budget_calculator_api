import logging

from fastapi import Depends, HTTPException

from api.core.security import get_password_hash
from api.schemas.user_schemas import User, UserCreate
from api.services.base_service import BaseService
from api.utils.uow import IUnitOfWork, UnitOfWork

logger = logging.getLogger(__name__)


class UserService(BaseService):
    async def add_user(self, user: UserCreate) -> User:
        user.password = get_password_hash(user.password)
        async with self.uow:
            user_from_db = await self.uow.user.add_one(user.model_dump())
            user_to_return = User.model_validate(user_from_db)
            await self.uow.commit()
            return user_to_return

    async def get_user(self, **kwargs) -> User | None:
        async with self.uow:
            user_from_db = await self.uow.user.get_one(**kwargs)
            return User.model_validate(user_from_db) if user_from_db else None

    async def get_users(self, **kwargs) -> list[User]:
        async with self.uow:
            users: list = await self.uow.user.get_all(**kwargs)
            return [User.model_validate(user) for user in users]

    async def count_users(self, **kwargs) -> int:
        async with self.uow:
            return await self.uow.user.count(**kwargs)

    async def get_user_or_404(self, **kwargs) -> User:
        user = await self.get_user(**kwargs)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found or token expired"
            )

        return user


async def get_user_service(
        uow: IUnitOfWork = Depends(UnitOfWork)
) -> UserService:
    return UserService(uow)
