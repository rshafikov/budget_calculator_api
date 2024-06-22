from typing import List

from fastapi import APIRouter, Depends

from api.routers.auth import rbac
from api.schemas.record_schemas import (RecordCreate, RecordExternal,
                                        RecordRequest)
from api.schemas.user_schemas import Role
from api.services.category_service import CategoryService, get_category_service
from api.services.record_service import RecordService, get_record_service
from api.services.user_service import UserService, get_user_service

record_router = APIRouter(prefix="/records", tags=["records"])


@record_router.get("/")
async def get_records(
    user_payload: dict = Depends(rbac({Role.USER})),
    user_service: UserService = Depends(get_user_service),
    record_service: RecordService = Depends(get_record_service),
) -> List[RecordExternal]:
    user = await user_service.get_user_or_404(telegram_id=user_payload['sub'])
    return await record_service.get_instances(user_id=user.id)


@record_router.post("/")
async def create_record(
        record: RecordRequest,
        user_payload: dict = Depends(rbac({Role.USER})),
        user_service: UserService = Depends(get_user_service),
        category_service: CategoryService = Depends(get_category_service),
        record_service: RecordService = Depends(get_record_service)
) -> RecordExternal:
    user = await user_service.get_user_or_404(telegram_id=user_payload['sub'])
    category = await category_service.get_instance_or_404(
        user_id=user.id,
        name=record.category_name,
        error_msg=f'Category {record.category_name!r} not found'
    )
    return await record_service.create_instance(
        RecordCreate(
            user_id=user.id,
            category_id=category.id,
            currency=record.currency if record.currency else user.currency,
            amount=record.amount
        )
    )
