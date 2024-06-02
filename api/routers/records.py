from fastapi import APIRouter

record_router = APIRouter(prefix="/records", tags=["records"])


@record_router.get("/")
async def get_records():
    pass


@record_router.post("/")
async def create_record():
    pass
