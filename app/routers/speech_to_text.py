import tempfile
from typing import Annotated

from celery import chain
from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi.responses import JSONResponse

from app.celery import transcribe, translate
from app.config import Settings
from app.deps import get_settings

router = APIRouter(prefix="/speech_to_text")


@router.post("/")
def speech_to_text(
    file: UploadFile,
    target_language: Annotated[str, Form()],
    settings: Settings = Depends(get_settings),
) -> JSONResponse:
    audio_file = tempfile.NamedTemporaryFile(delete=False)
    audio_file.write(file.file.read())
    audio_file.close()

    # task = transcribe.delay(  # type: ignore
    #     settings.whisper_model, settings.whisper_device, audio_file.name
    # )
    res = chain(
        transcribe.s(
            settings.whisper_model, settings.whisper_device, audio_file.name
        ),
        translate.s(target_language),
    )()
    return JSONResponse(
        {"transcription_task": res.parent.id, "translation_task": res.id}
    )
