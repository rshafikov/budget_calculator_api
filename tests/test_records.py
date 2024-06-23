import pytest
from fastapi import status

from api.core import settings


@pytest.mark.skipif(
    not settings.DB_TEST,
    reason='Setup test db instead of running production.'
)
class TestRecords:
    async def test_create_record(self, auth_client, db_manager, default_user, default_category):
        new_record = {
            'amount': 7,
            'category_name': default_category.name,
            'currency': default_user.currency.value,
        }
        records_before = await db_manager.record.count_instances(
            user_id=default_user.id
        )
        response = await auth_client.post('/records/', json=new_record)
        records_after = await db_manager.category.count_instances(
            user_id=default_user.id
        )

        assert records_after == records_before + 1
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['amount'] == new_record['amount']
        assert response.json()['category']['name'] == new_record['category_name']
        assert response.json()['amount'] == new_record['amount']

    async def test_create_same_record(self, auth_client, default_record, default_category):
        same_record = {
            'category_name': default_category.name,
            'amount': default_record.amount,
            'currency': default_record.currency.value
        }
        response = await auth_client.post('/records/', json=same_record)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['amount'] == same_record['amount']
        assert response.json()['category']['name'] == same_record['category_name']
        assert response.json()['amount'] == same_record['amount']

    async def test_get_records(self, auth_client, default_record):
        response = await auth_client.get('/records/')

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert len(response.json()) >= 1
