from api.db.models import CurrencyModel
from api.repositories.base_repository import Repository


class CurrencyRepository(Repository):
    model = CurrencyModel
