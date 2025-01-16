from app.message_broker_producer import MessageBrokerProducer
from unittest.mock import AsyncMock, patch
import pytest_asyncio
import pytest


DATA = {
    'id': 1,
    'user_name': 'Test Application',
    'description': 'This is a test application',
    'created_at': '2025...',
}


@pytest_asyncio.fixture
async def mock_producer(mocker):
    with patch.dict(
        'os.environ',
        {
            'BROKER_HOST': 'kafka',
            'BROKER_PORT': '9092',
            'APPLICATIONS_TOPIC_NAME': 'my_topic',
        },
    ):
        mock_producer = AsyncMock()
        mocker.patch(
            'app.message_broker_producer.AIOKafkaProducer',
            autospec=True,
            return_value=mock_producer,
        )
        broker = MessageBrokerProducer()
        async with broker as broker_instance:
            yield broker_instance, mock_producer


@pytest.mark.asyncio
async def test_send_data(mock_producer):
    broker, mock_producer = mock_producer
    await broker.create_application(DATA)
    mock_producer.send_and_wait.assert_awaited_once_with('my_topic', DATA)


@pytest.mark.asyncio
async def test_send_data_error(mock_producer):
    broker, mock_producer = mock_producer
    mock_producer.send_and_wait.side_effect = Exception('Producer Error')
    result = await broker.create_application(DATA)
    assert result is None
    mock_producer.send_and_wait.assert_awaited_once_with('my_topic', DATA)
