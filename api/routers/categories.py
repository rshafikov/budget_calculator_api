from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from api.routers.auth import rbac
from api.schemas.category_schemas import CategoryBase, CategoryCreate
from api.schemas.user_schemas import Role
from api.services.category_service import CategoryService, get_category_service
from api.services.user_service import UserService, get_user_service

category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category_for_user(
        category: CategoryBase,
        user_payload: dict = Depends(rbac({Role.USER})),
        category_service: CategoryService = Depends(get_category_service),
        user_service: UserService = Depends(get_user_service)
) -> CategoryBase:
    user = await user_service.get_user_or_404(telegram_id=user_payload["sub"])
    new_category = CategoryCreate(
        user_id=user.id,
        name=category.name,
        symbol=category.symbol
    )
    try:
        return await category_service.create_instance(instance=new_category)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'This category {category.name} already exists.'
        )


@category_router.get("/")
async def get_user_categories(
        user_payload: dict = Depends(rbac({Role.USER})),
        category_service: CategoryService = Depends(get_category_service),
        user_service: UserService = Depends(get_user_service)
) -> list[CategoryBase]:
    user = await user_service.get_user_or_404(telegram_id=user_payload["sub"])
    return await category_service.get_instances(user_id=user.id)
