from app.providers.whisper import Whisper
from app.utils.subtitle_formatter import SRTFormatter


class TranscribeUseCase:
    def __init__(self, whisper_model: str, whisper_device: str):
        self._whisper = Whisper(whisper_model, whisper_device)

    def execute(self, audio_path: str) -> tuple[str, str]:
        language, segments = self._whisper.transcribe(audio_path)
        formatter = SRTFormatter()
        return language, formatter.format(segments)
