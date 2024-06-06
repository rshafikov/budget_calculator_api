import pytest


class TestIndex:

    @pytest.mark.asyncio
    async def test_root(self, client):
        response = await client.get('/')

        assert response.status_code == 200
        assert response.json() == {'message': 'Welcome to the project API!'}
