import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from api.exceptions.exc_handlers import add_exc_handlers
from api.routers.auth import auth_router
from api.routers.categories import category_router
from api.routers.currency import currency_router
from api.routers.records import record_router
from api.routers.users import user_router

app = FastAPI(root_path='/api/v1')

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(currency_router)
app.include_router(record_router)

add_exc_handlers(app)


@app.get('/')
async def index() -> RedirectResponse:
    return RedirectResponse('/docs')


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000)
