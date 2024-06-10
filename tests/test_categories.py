import pytest
from fastapi import status

from api.core import settings
from api.schemas.category_schemas import CategoryCreate


@pytest.mark.skipif(
    not settings.DB_TEST,
    reason='Setup test db instead of running production.'
)
class TestCategories:
    @pytest.mark.asyncio
    async def test_create_category(self, auth_client, default_user, db_manager):
        new_category = {'name': 'test_category', 'symbol': '✅'}
        categories_before = await db_manager.category.count_categories(
            user_id=default_user.id
        )
        response = await auth_client.post('/categories/', json=new_category)
        categories_after = await db_manager.category.count_categories(
            user_id=default_user.id
        )

        assert categories_after == categories_before + 1
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == new_category

    @pytest.mark.asyncio
    async def test_get_categories(self, auth_client, default_user, db_manager):
        categories = await db_manager.category.get_categories(
            user_id=default_user.id)
        response = await auth_client.get('/categories/')

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert response.json() == categories

    @pytest.mark.asyncio
    async def test_categories_protected(self, client):
        get_response = await client.get('/categories/')
        post_response = await client.post(
            '/categories/',
            json={'name': 'test_category', 'symbol': '✅'}
        )

        assert get_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert post_response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_create_same_category(
            self, auth_client, default_user, db_manager
    ):
        new_category = {
            'name': 'test_category',
            'symbol': '✅',
            'user_id': default_user.id
        }
        category = await db_manager.category.create_category(
            CategoryCreate(**new_category))
        categories_before = await db_manager.category.count_categories(
            user_id=default_user.id
        )
        response = await auth_client.post('/categories/', json=new_category)
        categories_after = await db_manager.category.count_categories(
            user_id=default_user.id
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert categories_after == categories_before
        assert response.json()['detail'] == (
            f'This category {category.name} already exists.')
