from api.db.models import UserModel
from api.repositories.base_repository import Repository


class UserRepository(Repository):
    model = UserModel
