from fastapi import Depends

from api.schemas.category_schemas import Category
from api.services.base_service import BaseService
from api.utils.uow import IUnitOfWork, UnitOfWork


class CategoryService(BaseService):
    manager_name = 'category'
    default_result_schema = Category


async def get_category_service(
        uow: IUnitOfWork = Depends(UnitOfWork)
) -> CategoryService:
    return CategoryService(uow)
