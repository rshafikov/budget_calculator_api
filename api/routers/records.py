from datetime import date
from typing import Annotated, List

from fastapi import APIRouter, Query, status

from api.schemas.currency_schemas import Currency
from api.schemas.record_schemas import (RecordCreate, RecordExternal,
                                        RecordRequest)
from api.utils.dependencies import (CategoryServiceDeps, CurrentUserDeps,
                                    RecordServiceDeps)

record_router = APIRouter(prefix="/records", tags=["records"])


@record_router.get("/")
async def get_records(
    user: CurrentUserDeps,
    record_service: RecordServiceDeps,
    _from: Annotated[date | None, Query(alias='from')] = None,
    _to: Annotated[date | None, Query(alias='to')] = None
) -> List[RecordExternal]:
    return await record_service.filter(_from, _to, user_id=user.id)


@record_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_record(
        record: RecordRequest,
        user: CurrentUserDeps,
        category_service: CategoryServiceDeps,
        record_service: RecordServiceDeps,
        currency: Annotated[Currency | None, Query(max_length=3)] = None,
) -> RecordExternal:
    category = await category_service.get_instance_or_404(
        user_id=user.id,
        name=record.category_name,
        error_msg=f'Category {record.category_name!r} not found'
    )
    return await record_service.create_instance(
        RecordCreate(
            user_id=user.id,
            category_id=category.id,
            currency=currency if currency is not None else user.currency,
            amount=record.amount
        )
    )
