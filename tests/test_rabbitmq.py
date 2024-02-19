from unittest.mock import ANY, MagicMock

import pytest
from pytest_mock import MockerFixture

from app.config import Settings
from app.loaders.rabbitmq import MessageSender


@pytest.fixture(scope="module")
def settings() -> Settings:
    return Settings(
        minio_host="host",
        minio_access_key="access",
        minio_secret_key="secret",
        minio_bucket_name="bucket",
        rabbitmq_url="url",
        rabbitmq_queue_name="queue",
    )


@pytest.mark.asyncio
async def test_send(settings: Settings, mocker: MockerFixture):
    mock = mocker.patch("app.loaders.rabbitmq.connect")
    message_sender = MessageSender(settings)
    msg = "test"
    await message_sender.send(msg)
    mock.assert_called_once_with(
        settings.rabbitmq_url,
    )
    mock_channel: MagicMock = mock.return_value.channel.return_value
    mock_channel.declare_queue.assert_called_once_with(
        settings.rabbitmq_queue_name
    )
    mock_channel.default_exchange.publish.assert_called_once_with(
        ANY,
        routing_key=mock_channel.declare_queue.return_value.name,
    )
