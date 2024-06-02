import uvicorn
from fastapi import FastAPI

from api.routers.auth import auth_router
# from api.routers.records import record_router
from api.routers.users import users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(auth_router)
# app.include_router(us)

if __name__ == "__main__":
    uvicorn.run(app="main:app")
