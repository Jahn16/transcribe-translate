from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from app.config import Settings
from app.providers.whisper import Whisper


@pytest.fixture
def settings() -> Settings:
    return Settings(whisper_model="base", whisper_device="cpu")


@pytest.fixture
def model_size() -> str:
    return "small"


@pytest.fixture
def device() -> str:
    return "cpu"


@pytest.fixture
def audio() -> str:
    return "audio.mp3"


def test_translate(
    audio: str, model_size: str, device: str, mocker: MockerFixture
) -> None:
    whisper = Whisper(model_size, device)
    whisper_mock = mocker.patch("app.providers.whisper.WhisperModel")
    segments_mock, info_mock = ([MagicMock()], MagicMock())
    lang = "de"
    info_mock.language = lang
    whisper_mock().transcribe.return_value = (segments_mock, info_mock)
    result = whisper.transcribe(audio)
    whisper_mock.assert_called_with(
        model_size, device=device
    )
    whisper_mock().transcribe.assert_called_once_with(audio)
    assert result == (lang, segments_mock)
