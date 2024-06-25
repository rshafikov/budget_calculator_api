from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from api.schemas.category_schemas import CategoryBase, CategoryCreate
from api.utils.dependencies import CategoryServiceDeps, CurrentUserDeps

category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category_for_user(
        current_user: CurrentUserDeps,
        category: CategoryBase,
        category_manager: CategoryServiceDeps,
) -> CategoryBase:
    new_category = CategoryCreate(
        user_id=current_user.id,
        name=category.name,
        symbol=category.symbol
    )
    try:
        return await category_manager.create_instance(instance=new_category)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'This category {category.name} already exists.'
        )


@category_router.get("/")
async def get_user_categories(
        user: CurrentUserDeps,
        category_service: CategoryServiceDeps,
) -> list[CategoryBase]:
    return await category_service.get_instances(user_id=user.id)
