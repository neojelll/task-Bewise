from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from app.api import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest_asyncio.fixture
async def mock_producer(mocker):
    mock_broker = mocker.patch('app.api.MessageBrokerProducer', autospec=True)
    mock_broker_instance = mock_broker.return_value
    mock_broker_instance.__aenter__.return_value = mock_broker_instance
    return mock_broker_instance


@pytest_asyncio.fixture
async def mock_db(mocker):
    mock_db = mocker.patch('app.api.DataBase', autospec=True)
    mock_db_instance = mock_db.return_value
    mock_db_instance.__aenter__.return_value = mock_db_instance
    return mock_db_instance


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'application_data, database_return, expected_code',
    [
        (
            {
                'user_name': 'Test Application',
                'description': 'This is a test application',
            },
            {
                'id': 1,
                'user_name': 'Test Application',
                'description': 'This is a test application',
                'created_at': '2025...',
            },
            status.HTTP_200_OK,
        ),
        (
            {
                'user_name': 'Test Application',
                'description': 'This is a test application',
            },
            None,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
    ],
)
async def test_create_application(
    client, mock_db, mock_producer, application_data, database_return, expected_code
):
    mock_producer_instance = mock_producer
    mock_producer_instance.create_application = AsyncMock()

    mock_database_instance = mock_db
    mock_database_instance.create_application = AsyncMock(return_value=database_return)

    application_data = application_data

    response = client.post('/applications', json=application_data)

    assert response.status_code == expected_code

    if database_return:
        assert 'id' in response.json()
        assert 'created_at' in response.json()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'database_return, expected_code',
    [
        (
            {
                'page': 1,
                'size': 10,
                'total': 1,
                'applications': [
                    {
                        'id': 1,
                        'user_name': 'Test Application',
                        'description': 'This is a test application',
                        'created_at': '112',
                    }
                ],
            },
            status.HTTP_200_OK,
        ),
        (None, status.HTTP_500_INTERNAL_SERVER_ERROR),
    ],
)
async def test_get_applications(client, mock_db, database_return, expected_code):
    mock_database_instance = mock_db
    mock_database_instance.get_applications = AsyncMock(return_value=database_return)
    response = client.get('/applications')
    assert response.status_code == expected_code
    assert isinstance(response.json(), dict)
