import logging
import asyncio
from fastapi import APIRouter
from app.services.queue import queue_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/status/ok")
async def status_ok():
    """AI 서버 상태를 READY로 변경 후 자동 큐 처리"""
    queue_service.set_ai_status(True)
    logger.info("🟢 [AI 서버 READY] 큐 자동 처리 시작")

    if not queue_service.is_worker_running and not queue_service.request_queue.empty():
        asyncio.create_task(queue_service.process_queue())

    return {"message": "AI server marked as READY. Processing queued requests."}