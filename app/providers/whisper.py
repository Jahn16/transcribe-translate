from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment

from app.config import Settings


class Whisper:
    def __init__(self, settings: Settings):
        self._model_size = settings.whisper_model
        self._device = settings.whisper_device

    def transcribe(self, audio_path: str) -> list[Segment]:
        model = WhisperModel(self._model_size, device=self._device)
        segments, _ = model.transcribe(audio_path)
        return list(segments)
