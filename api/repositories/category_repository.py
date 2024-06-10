from api.db.models import CategoryModel
from api.repositories.base_repository import Repository


class CategoryRepository(Repository):
    model = CategoryModel
