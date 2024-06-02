from fastapi import APIRouter
from api.schemas.category_schemas import CategoryCreate


record_router = APIRouter(prefix="/categories", tags=["categories"])


@record_router.post("/")
async def create_catergory_for_user():
    pass


@record_router.get("/")
async def get_user_categories():
    pass
