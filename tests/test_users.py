import pytest
from fastapi import status

from api.core import settings
from api.schemas.user_schemas import UserCreate

PROTECTED_ROUTES = [
    ('/users/me', 'GET'), ('/users/test_user/', 'GET'), ('/users/', 'GET')
]

PUBLIC_ROUTES = [('/users/', 'POST')]


@pytest.mark.skipif(
    not settings.DB_TEST,
    reason='Setup test db instead of running production.'
)
class TestUsers:
    @pytest.mark.asyncio
    async def test_user_own_profile(self, auth_client, test_user: UserCreate):
        response = await auth_client.get('/users/me')

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['telegram_id'] == test_user.telegram_id
        assert response.json()['name'] == test_user.name
        assert response.json()['lastname'] == test_user.lastname

    @pytest.mark.asyncio
    @pytest.mark.parametrize('route, method', PROTECTED_ROUTES)
    async def test_protected_endpoints(self, method, route, client):
        response = await client.request(method, route)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()['detail'] == 'Not authenticated'

    @pytest.mark.asyncio
    @pytest.mark.parametrize('route, method', PUBLIC_ROUTES)
    async def test_public_endpoints(self, method, route, client):
        response = await client.request(method, route)

        assert response.status_code != status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_create_user(self, client, db_manager):
        users_before = await db_manager.user.count_users()
        new_user = {'telegram_id': '1234', 'name': 'user', 'password': 'pass'}
        response = await client.post('/users/', json=new_user)
        users_after = await db_manager.user.count_users()

        assert users_before + 1 == users_after
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['telegram_id'] == new_user['telegram_id']
        assert response.json()['name'] == new_user['name']

    @pytest.mark.asyncio
    async def test_get_test_user(self, auth_client, test_user, mock_token):
        response = await auth_client.get(f'/users/{test_user.telegram_id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['telegram_id'] == test_user.telegram_id

    @pytest.mark.asyncio
    async def test_get_users(self, auth_client, test_user, mock_token):
        response = await auth_client.get('/users/')

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1
