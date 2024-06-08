import pytest
from fastapi import status

from api.core import settings


@pytest.mark.skipif(
    not settings.DB_TEST,
    reason='Setup test db instead of running production.'
)
class TestAuth:
    @pytest.mark.asyncio
    async def test_create_token(self, client, test_user, default_user):
        user_form = {
            'username': test_user.telegram_id,
            'password': test_user.password
        }
        response = await client.post('/auth/token', data=user_form)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get('access_token') is not None
        assert response.json()['token_type'] == 'bearer'
