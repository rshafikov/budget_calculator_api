import time
from dataclasses import dataclass

import pytest
from httpx import ASGITransport, AsyncClient

from api.core.security import create_token
from api.db.database import engine
from api.db.models import BaseModel
from api.main import app
from api.routers.auth import check_token
from api.schemas.currency_schemas import CurrencyBase
from api.schemas.user_schemas import UserCreate
from api.services.category_service import CategoryService, get_category_service
from api.services.currency_service import CurrencyService, get_currency_service
from api.services.user_service import UserService, get_user_service
from api.utils.uow import UnitOfWork


@dataclass(frozen=True)
class TestDBManager:
    user: UserService
    category: CategoryService
    currency: CurrencyService


@pytest.fixture()
async def test_user() -> UserCreate:
    return UserCreate(
        telegram_id='test_user',
        password='pass',
        name='test_user_name',
        lastname='test_user_lastname'
    )


@pytest.fixture()
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        yield
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest.fixture()
async def db_manager(create_db):
    uow = UnitOfWork()
    user_service = await get_user_service(uow)
    category_service = await get_category_service(uow)
    currency_service = await get_currency_service(uow)

    yield TestDBManager(
        user=user_service,
        category=category_service,
        currency=currency_service
    )


@pytest.fixture()
async def default_user(db_manager: TestDBManager, test_user: UserCreate):
    user = await db_manager.user.add_user(test_user.model_copy(deep=True))
    yield user


@pytest.fixture()
async def auth_client(default_user: UserCreate):
    token = create_token(default_user.telegram_id)
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://test',
            headers={'Authorization': f'Bearer {token}'}
    ) as authorized_client:
        yield authorized_client


@pytest.fixture()
async def client(create_db):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture()
async def mock_token():
    admin_token = {
        'exp': int(time.time() + 60),
        'role': 'admin',
        'sub': 'test_user'
    }
    app.dependency_overrides[check_token] = lambda: admin_token
    yield admin_token
    app.dependency_overrides = {}


@pytest.fixture()
async def default_currency(db_manager: TestDBManager):
    euro = await db_manager.currency.create_instance(
        CurrencyBase(name='EUR', symbol='€'))
    yield euro
