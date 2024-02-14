from typing import Annotated

from fastapi import APIRouter, Form, UploadFile

router = APIRouter(prefix="/speech_to_text")


@router.post("/")
async def speech_to_text(
    file: UploadFile, target_language: Annotated[str, Form()]
) -> dict[str, bool]:
    return {"sucess": True}
