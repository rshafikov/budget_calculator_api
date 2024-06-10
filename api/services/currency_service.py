from fastapi import Depends

from api.utils.uow import IUnitOfWork, UnitOfWork


class CurrencyService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow


async def get_user_service(
        uow: IUnitOfWork = Depends(UnitOfWork)
) -> CurrencyService:
    return CurrencyService(uow)
