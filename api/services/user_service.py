import logging

from fastapi import Depends

from api.core.security import get_password_hash
from api.schemas.user_schemas import AdminCreate, User, UserCreate
from api.services.base_service import BaseService
from api.utils.uow import IUnitOfWork, UnitOfWork

logger = logging.getLogger(__name__)


class UserService(BaseService):
    manager_name = 'user'
    default_result_schema = User

    async def add_user(self, user: UserCreate | AdminCreate) -> User:
        user.password = get_password_hash(user.password)
        return await self.create_instance(instance=user)

    async def get_user(self, **kwargs) -> User | None:
        return await self.get_instance(**kwargs)

    async def get_user_or_404(self, **kwargs):
        return await self.get_instance_or_404(
            error_msg='User not found or token expired', **kwargs
        )


async def get_user_service(
        uow: IUnitOfWork = Depends(UnitOfWork)
) -> UserService:
    return UserService(uow)
