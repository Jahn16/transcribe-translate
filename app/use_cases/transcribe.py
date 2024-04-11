from app.providers.whisper import Whisper


class TranscribeUseCase:
    def __init__(self, whisper_model: str, whisper_device: str):
        self._whisper = Whisper(whisper_model, whisper_device)

    def execute(self, audio_path: str) -> tuple[str, list[str]]:
        language, segments = self._whisper.transcribe(audio_path)
        return language, [segment.text for segment in segments]
