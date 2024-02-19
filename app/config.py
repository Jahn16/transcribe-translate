from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # type: ignore
    minio_host: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket_name: str
    rabbitmq_url: str
    rabbitmq_queue_name: str
