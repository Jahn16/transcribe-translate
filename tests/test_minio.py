from io import BytesIO

import pytest
from pytest_mock import MockerFixture

from app.config import Settings
from app.repositories.minio import MinioRepository


@pytest.fixture(scope="module")
def settings():
    return Settings(
        minio_host="host",
        minio_access_key="access",
        minio_secret_key="secret",
        minio_bucket_name="bucket",
    )


@pytest.fixture
def file_data():
    data = BytesIO(b"data")
    file_name = "test.file"
    file_size = 3

    return (file_name, data, file_size)


def test_upload_file(
    settings: Settings,
    file_data: tuple[BytesIO, str, int],
    mocker: MockerFixture,
):
    mock = mocker.patch("app.repositories.minio.Minio")
    repo = MinioRepository(settings)

    mock().bucket_exists.return_value = True
    repo.upload_file(*file_data)

    mock().put_object.assert_called_once_with(
        settings.minio_bucket_name, *file_data
    )
    mock().make_bucket.assert_not_called()


def test_upload_file_no_bucket(
    settings: Settings,
    file_data: tuple[BytesIO, str, int],
    mocker: MockerFixture,
):
    mock = mocker.patch("app.repositories.minio.Minio")
    repo = MinioRepository(settings)

    mock().bucket_exists.return_value = False
    repo.upload_file(*file_data)

    mock().make_bucket.assert_called_once_with(settings.minio_bucket_name)
    mock().put_object.assert_called_once_with(
        settings.minio_bucket_name, *file_data
    )


def test_get_presigned_url(settings: Settings, mocker: MockerFixture):
    mock = mocker.patch("app.repositories.minio.Minio")
    repo = MinioRepository(settings)

    mock().presigned_get_object.return_value = "url"

    url = repo.get_presigned_url("file_name")

    mock().presigned_get_object.assert_called_once_with(
        "http", settings.minio_bucket_name, "file_name"
    )
    assert url == "url"
