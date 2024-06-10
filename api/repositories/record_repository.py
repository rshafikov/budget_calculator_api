from api.db.models import RecordModel
from api.repositories.base_repository import Repository


class RecordRepository(Repository):
    model = RecordModel
