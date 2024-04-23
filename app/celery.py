from celery import Celery

from app.providers.translate import ArgosTranslate
from app.use_cases.transcribe import TranscribeUseCase
from app.use_cases.translate import TranslateUseCase

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)


@app.task
def transcribe(
    whisper_model: str, whisper_device: str, audio_path: str
) -> tuple[str, str]:
    use_case = TranscribeUseCase(whisper_model, whisper_device)
    result = use_case.execute(audio_path)
    return result


@app.task
def translate(input: tuple[str, str], to_lang: str) -> str:
    from_lang, sentences = input
    translator = ArgosTranslate()
    use_case = TranslateUseCase(translator)
    return use_case.execute(sentences, from_lang, to_lang)
