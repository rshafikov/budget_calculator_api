from fastapi import APIRouter, Depends, HTTPException, status

from api.routers.auth import rbac
from api.schemas.user_schemas import Role, UserBase, UserCreate, UserSecure
from api.services.user_service import UserService, get_user_service

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        new_user: UserCreate,
        user_service: UserService = Depends(get_user_service)
) -> UserBase:
    db_user = await user_service.get_user(telegram_id=new_user.telegram_id)

    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    return await user_service.add_user(new_user)


@user_router.get("/", dependencies=[Depends(rbac({Role.ADMIN}))])
async def get_users(
    offset: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
) -> list[UserBase]:
    return await user_service.get_instances(offset=offset, limit=limit)


@user_router.get("/{tg_id}/", dependencies=[Depends(rbac({Role.ADMIN}))])
async def get_user(
        tg_id: str,
        user_service: UserService = Depends(get_user_service)
) -> UserBase:
    return await user_service.get_user_or_404(telegram_id=tg_id)


@user_router.get("/me")
async def user_profile(
    user_service: UserService = Depends(get_user_service),
    user_payload: dict = Depends(rbac({Role.USER})),
) -> UserSecure:
    return await user_service.get_user_or_404(telegram_id=user_payload["sub"])
