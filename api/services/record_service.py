from datetime import date

from fastapi import Depends

from api.schemas.record_schemas import Record
from api.services.base_service import BaseService
from api.utils.uow import IUnitOfWork, UnitOfWork


class RecordService(BaseService):
    manager_name = 'record'
    default_result_schema = Record

    async def filter(
            self,
            _from: date | None,
            _to: date | None = None,
            **kwargs
    ) -> list[Record]:
        if _from or _to:
            async with self.uow:
                manager = getattr(self.uow, self.manager_name)
                instances = await manager.filter_by_date(_from, _to, **kwargs)
                return [self.default_result_schema.model_validate(i)
                        for i in instances]

        return await self.get_instances(**kwargs)


async def get_record_service(
        uow: IUnitOfWork = Depends(UnitOfWork)
) -> RecordService:
    return RecordService(uow)
