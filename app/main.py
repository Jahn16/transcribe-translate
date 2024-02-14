from fastapi import APIRouter, FastAPI

from app.routers import speech_to_text

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(speech_to_text.router)

app.include_router(api_router)
