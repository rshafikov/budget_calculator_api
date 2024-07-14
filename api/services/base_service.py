from typing import Any

from fastapi import HTTPException

from api.core.security import sanitize_args
from api.utils.uow import IUnitOfWork


class BaseService:
    manager_name: None
    default_result_schema: None

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def create_instance(self, instance):
        async with self.uow:
            manager = getattr(self.uow, self.manager_name)
            new = await manager.add_one(instance.model_dump())
            created = self.default_result_schema.model_validate(new)
            await self.uow.commit()
            return created

    async def get_instance(self, raw_model: bool = False, **kwargs):
        async with self.uow:
            manager = getattr(self.uow, self.manager_name)
            instance = await manager.get_one(**kwargs)
            if raw_model:
                return instance

            return self.default_result_schema.model_validate(
                instance) if instance else None

    async def get_instances(self, **kwargs) -> list[Any]:
        async with self.uow:
            manager = getattr(self.uow, self.manager_name)
            instances: list = await manager.get_all(**kwargs)
            return [self.default_result_schema.model_validate(i)
                    for i in instances]

    async def count_instances(self, **kwargs) -> int:
        async with self.uow:
            manager = getattr(self.uow, self.manager_name)
            return await manager.count(**kwargs)

    async def update_instance(self, instance_id, data: dict):
        async with self.uow:
            manager = getattr(self.uow, self.manager_name)
            update = await manager.update_one(instance_id, data)
            updated = self.default_result_schema.model_validate(update)
            await self.uow.commit()
            return updated

    async def delete_instance(self, instance=None, **kwargs) -> None:
        async with self.uow:
            manager = getattr(self.uow, self.manager_name)
            await manager.delete_one(instance=instance, **kwargs)
            await self.uow.commit()

    async def get_instance_or_404(self, raw_model: bool = False, **kwargs) -> Any:
        error_msg = kwargs.pop('error_msg', None)
        instance = await self.get_instance(raw_model=raw_model, **kwargs)

        if not instance:
            if error_msg is None:
                req_args = kwargs.copy()
                error_msg = (
                    f'Instance with parameters: {sanitize_args(req_args)!r} '
                    f'not found in '
                    f'{self.default_result_schema.__name__.replace("DB", "")}'
                )

            raise HTTPException(status_code=404, detail=error_msg)

        return instance
