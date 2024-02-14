import abc
from typing import BinaryIO

from app.config import Settings


class BaseRepository(abc.ABC):
    @abc.abstractmethod
    def upload_file(
        self, data: BinaryIO, file_name: str, file_size: int
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_presigned_url(self, file_name: str) -> str:
        raise NotImplementedError


class MinioRepository(BaseRepository):
    def __init__(self, settings: Settings):
        pass

    def upload_file(
        self, data: BinaryIO, file_name: str, file_size: int
    ) -> None:
        pass

    def get_presigned_url(self, file_name: str) -> str:
        return ""
