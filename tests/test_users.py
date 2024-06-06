import pytest

from api.core import settings


@pytest.mark.skipif(
    not settings.DB_TEST,
    reason='Setup test db instead of production.'
)
class TestUsers:
    @pytest.mark.asyncio
    async def test_user_own_profile(self, auth_client, test_user):
        response = await auth_client.get('/users/me')

        assert response.status_code == 200
        assert response.json()['telegram_id'] == test_user.telegram_id
