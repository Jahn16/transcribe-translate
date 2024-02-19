import abc

from aio_pika import Message, connect

from app.config import Settings


class BaseMessageSender(abc.ABC):
    def __init__(self, settings: Settings) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, message: str) -> None:
        raise NotImplementedError


class MessageSender(BaseMessageSender):
    def __init__(self, settings: Settings) -> None:
        self._url = settings.rabbitmq_url
        self._queue_name = settings.rabbitmq_queue_name

    async def send(self, message: str) -> None:
        connection = await connect(self._url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(self._queue_name)
            await channel.default_exchange.publish(
                Message(bytes(message, "utf-8")),
                routing_key=queue.name,
            )
