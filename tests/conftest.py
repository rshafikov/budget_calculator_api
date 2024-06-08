import time

import pytest
from httpx import ASGITransport, AsyncClient

from api.core.security import create_token
from api.db.database import engine
from api.db.models import BaseModel
from api.main import app
from api.routers.auth import check_token
from api.schemas.user_schemas import UserCreate
from api.services.user_service import UserService, get_user_service
from api.utils.uow import UnitOfWork


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
async def user_manager(create_db):
    manager = await get_user_service(UnitOfWork())
    yield manager


@pytest.fixture()
async def default_user(user_manager: UserService, test_user: UserCreate):
    user = await user_manager.add_user(test_user.model_copy(deep=True))
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
