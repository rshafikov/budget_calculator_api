import pytest

from api.core import settings


@pytest.mark.skipif(
    not settings.DB_TEST,
    reason='Setup test db instead of running production.'
)
class TestIndex:
    @pytest.mark.asyncio
    async def test_root(self, client):
        response = await client.get('/')

        assert response.status_code == 307
