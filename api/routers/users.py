from fastapi import APIRouter, Depends, HTTPException, status

from api.routers.auth import rbac
from api.schemas.user_schemas import Role, UserBase, UserCreate, UserSecure
from api.services.user_service import UserService, get_user_service

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@users_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserBase
)
async def create_user(
    new_user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    db_user = await user_service.get_user(telegram_id=new_user.telegram_id)

    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    return await user_service.add_user(new_user)


@users_router.get(
    "/",
    response_model=list[UserBase],
    dependencies=[Depends(rbac({Role.ADMIN}))]
)
async def get_users(
    offset: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_users(offset=offset, limit=limit)


@users_router.get(
    "/{user_tg_id}/",
    response_model=UserBase,
    dependencies=[Depends(rbac({Role.ADMIN}))],
)
async def get_user(
    user_tg_id: str, user_service: UserService = Depends(get_user_service)
):
    db_user = await user_service.get_user(telegram_id=user_tg_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@users_router.get("/me", response_model=UserSecure)
async def user_profile(
    user_service: UserService = Depends(get_user_service),
    user_token_payload: dict = Depends(rbac({Role.USER})),
):
    return await user_service.get_user(telegram_id=user_token_payload["sub"])
