import pytest
from fastapi import status

from api.core import settings


@pytest.mark.skipif(
    not settings.DB_TEST,
    reason='Setup test db instead of running production.'
)
class TestCurrency:
    @pytest.mark.asyncio
    async def test_create_currency(self, auth_client, db_manager, mock_token):
        new_currency = {'name': 'test_currency', 'symbol': '✅'}
        currency_before = await db_manager.currency.count_instances()
        response = await auth_client.post('/currency/', json=new_currency)
        currency_after = await db_manager.currency.count_instances()

        assert currency_after == currency_before + 1
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == new_currency

    @pytest.mark.asyncio
    async def test_get_currency(
            self, auth_client, default_currency, db_manager
    ):
        response = await auth_client.get(f'/currency/{default_currency.name}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'symbol': default_currency.symbol,
            'name': default_currency.name
        }

    @pytest.mark.asyncio
    async def test_currency_protected(self, default_currency, client):
        get_response = await client.get(f'/currency/{default_currency.name}/')
        post_response = await client.post(
            '/currency/',
            json={'name': 'test_currency', 'symbol': '✅'}
        )

        assert get_response.status_code == status.HTTP_401_UNAUTHORIZED
        assert post_response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_create_same_currency(
            self, auth_client, default_currency, db_manager, mock_token
    ):
        currency_before = await db_manager.currency.count_instances()
        response = await auth_client.post(
            '/currency/',
            json={
                'name': default_currency.name,
                'symbol': default_currency.symbol
            }
        )
        currency_after = await db_manager.currency.count_instances()

        # assert response.status_code == status.HTTP_409_CONFLICT
        assert currency_after == currency_before
        assert response.json()['detail'] == (
            f'This currency {default_currency.name} already exists.')
