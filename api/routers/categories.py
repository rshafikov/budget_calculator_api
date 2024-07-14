from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

from api.schemas.category_schemas import CategoryBase, CategoryCreate
from api.utils.dependencies import (CategoryServiceDeps, CurrentUserDeps,
                                    RecordServiceDeps)

category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.get("/")
async def get_user_categories(
        user: CurrentUserDeps,
        category_service: CategoryServiceDeps,
        hidden: Annotated[bool | None, Query()] = False,
) -> list[CategoryBase]:
    return await category_service.get_instances(user_id=user.id, hidden=hidden)


@category_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category_for_user(
        current_user: CurrentUserDeps,
        category: CategoryBase,
        manager: CategoryServiceDeps,
) -> CategoryBase:
    hidden_category = await manager.get_instance(
        name=category.name, user_id=current_user.id, hidden=True
    )
    if hidden_category:
        return await manager.update_instance(
            instance_id=hidden_category.id,
            data={'hidden': False, **category.model_dump()},
        )

    try:
        return await manager.create_instance(
            instance=CategoryCreate(
                user_id=current_user.id,
                name=category.name,
                symbol=category.symbol
            )
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Category with name {category.name!r} already exists.'
        )


@category_router.put("/{category_name}", status_code=status.HTTP_200_OK)
async def update_category(
        category_name: str,
        updated_category: CategoryBase,
        user: CurrentUserDeps,
        manager: CategoryServiceDeps,
) -> CategoryBase:
    category = await manager.get_instance_or_404(
        name=category_name, user_id=user.id, hidden=False
    )
    return await manager.update_instance(category.id, updated_category.model_dump())


@category_router.delete("/{category_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        category_name: str,
        user: CurrentUserDeps,
        category_manager: CategoryServiceDeps,
        record_manager: RecordServiceDeps
) -> None:
    category = await category_manager.get_instance_or_404(
        name=category_name, user_id=user.id, hidden=False
    )
    category_records = await record_manager.get_instances(category_id=category.id)
    if category_records:
        await category_manager.update_instance(
            instance_id=category.id, data={'hidden': True}
        )
    else:
        await category_manager.delete_instance(id=category.id)
