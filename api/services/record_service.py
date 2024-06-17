from fastapi import Depends

from api.schemas.record_schemas import Record
from api.services.base_service import BaseService
from api.utils.uow import IUnitOfWork, UnitOfWork


class RecordService(BaseService):
    manager_name = 'record'
    default_result_schema = Record


async def get_record_service(
        uow: IUnitOfWork = Depends(UnitOfWork)
) -> RecordService:
    return RecordService(uow)
