from celery.result import AsyncResult
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.celery import app

router = APIRouter(prefix="/tasks")


@router.get("/{task_id}")
def get_status(task_id: str):
    task_result = AsyncResult(task_id, app=app)
    return JSONResponse(
        {
            "id": task_id,
            "status": task_result.status,
            "result": task_result.result,
        }
    )
