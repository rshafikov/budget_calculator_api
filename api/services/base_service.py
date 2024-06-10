from api.utils.uow import IUnitOfWork


class BaseService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
