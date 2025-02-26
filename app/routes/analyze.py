import logging
import uuid
from fastapi import APIRouter, HTTPException
from app.type import AnalysisStartRequestDTO
from app.services.queue import queue_service

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/analyze/start")
async def analyze_start(request: AnalysisStartRequestDTO):
    """요청을 큐에 추가 후 자동 처리 시작"""
    request_id = str(uuid.uuid4())
    logger.info(f"📥 [요청 접수] Request ID: {request_id}")

    try:
        await queue_service.enqueue_request(request_id, request.model_dump())
        return True
    except Exception as e:
        logger.error(f"❌ 요청 실패 (Request ID: {request_id}): {e}")
        raise HTTPException(status_code=500, detail=f"Failed to queue request: {e}")
