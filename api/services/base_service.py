from typing import Any

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

    async def get_instance(self, **kwargs):
        async with self.uow:
            manager = getattr(self.uow, self.manager_name)
            instance = await manager.get_one(**kwargs)
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
