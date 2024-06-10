from fastapi import Depends

from api.schemas.category_schemas import Category, CategoryCreate
from api.services.base_service import BaseService
from api.utils.uow import IUnitOfWork, UnitOfWork


class CategoryService(BaseService):
    async def create_category(
            self, category: CategoryCreate) -> Category:
        async with self.uow:
            new_category = await self.uow.category.add_one(category.model_dump())
            created_category = Category.model_validate(new_category)
            await self.uow.commit()
            return created_category

    async def get_category(self, **kwargs) -> Category | None:
        async with self.uow:
            category = await self.uow.category.get_one(**kwargs)
            return Category.model_validate(category) if category else None

    async def get_categories(self, **kwargs) -> list[Category]:
        async with self.uow:
            categories: list = await self.uow.category.get_all(**kwargs)
            return [Category.model_validate(c) for c in categories]

    async def count_categories(self, **kwargs) -> int:
        async with self.uow:
            return await self.uow.category.count(**kwargs)


async def get_category_service(
        uow: IUnitOfWork = Depends(UnitOfWork)
) -> CategoryService:
    return CategoryService(uow)
