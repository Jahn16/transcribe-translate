import structlog
from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment

from app.config import Settings

logger = structlog.get_logger()


class Whisper:
    def __init__(self, settings: Settings):
        self._model_size = settings.whisper_model
        self._device = settings.whisper_device

    def transcribe(self, audio_path: str) -> tuple[str, list[Segment]]:
        model = WhisperModel(self._model_size, device=self._device)
        logger.info("Transcribing audio")
        segments, info = model.transcribe(audio_path)
        logger.info("Transcription finished")
        return info.language, list(segments)
