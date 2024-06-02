from fastapi import Depends

from api.core.security import get_password_hash
from api.schemas.user_schemas import User, UserCreate
from api.utils.uow import IUnitOfWork, UnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

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


async def get_user_service(
        uow: IUnitOfWork = Depends(UnitOfWork)
) -> UserService:
    return UserService(uow)
