from fastapi import APIRouter, FastAPI

from app.routers import speech_to_text, tasks
from app.utils.logging import setup_logging

setup_logging()

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(speech_to_text.router)
api_router.include_router(tasks.router)

app.include_router(api_router)
