import abc

from app.config import Settings


class BaseMessageSender(abc.ABC):
    def __init__(self, settings: Settings) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, message: str) -> None:
        raise NotImplementedError


class MessageSender(BaseMessageSender):
    def __init__(self, settings: Settings) -> None:
        pass

    async def send(self, message: str) -> None:
        pass
