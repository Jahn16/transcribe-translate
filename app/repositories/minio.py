import abc
from typing import BinaryIO

from minio import Minio

from app.config import Settings


class BaseRepository(abc.ABC):
    @abc.abstractmethod
    def upload_file(
        self, file_name: str, data: BinaryIO, file_size: int
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_presigned_url(self, file_name: str) -> str:
        raise NotImplementedError


class MinioRepository(BaseRepository):
    def __init__(self, settings: Settings):
        self._client = Minio(
            settings.minio_host,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
        )
        self._bucket_name = settings.minio_bucket_name

    def upload_file(
        self, file_name: str, data: BinaryIO, file_size: int
    ) -> None:
        if not self._client.bucket_exists(self._bucket_name):
            self._client.make_bucket(self._bucket_name)

        self._client.put_object(self._bucket_name, file_name, data, file_size)

    def get_presigned_url(self, file_name: str) -> str:
        return self._client.presigned_get_object(self._bucket_name, file_name)
