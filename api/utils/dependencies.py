from typing import Annotated

from fastapi import Depends

from api.routers.auth import get_auth_user
from api.schemas.user_schemas import User
from api.services.category_service import CategoryService, get_category_service
from api.services.record_service import RecordService, get_record_service
from api.services.user_service import UserService, get_user_service

CurrentUserDeps = Annotated[User, Depends(get_auth_user)]
UserServiceDeps = Annotated[UserService, Depends(get_user_service)]
CategoryServiceDeps = Annotated[CategoryService, Depends(get_category_service)]
RecordServiceDeps = Annotated[RecordService, Depends(get_record_service)]
