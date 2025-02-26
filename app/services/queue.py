import asyncio
import logging
from app.services.request import send_request_to_ai_server

logger = logging.getLogger(__name__)

class QueueService:
    def __init__(self, maxsize: int = 20):
        self.request_queue = asyncio.Queue(maxsize=maxsize)
        self.is_worker_running = False
        self.worker_lock = asyncio.Lock()
        self.AI_server_status = True

    async def enqueue_request(self, request_id: str, request_data: dict):
        """큐에 요청을 추가"""
        await self.request_queue.put((request_id, request_data))
        logger.info(f"📚 [큐에 추가됨] 위치: {self.request_queue.qsize()} | Request ID: {request_id}")

        # AI 서버가 READY 상태면 자동으로 큐 처리 시작
        if self.AI_server_status and not self.is_worker_running:
            asyncio.create_task(self.process_queue())
            

    async def process_queue(self):
        """큐에 있는 요청을 하나씩 처리"""
        async with self.worker_lock:
            if not self.AI_server_status or self.is_worker_running :
                logger.info("실행 중지")
                return  # 중복 실행 방지
            self.is_worker_running = True
            

        try:
            if not self.request_queue.empty() and self.AI_server_status:
                request_id, request_data = await self.request_queue.get()
                logger.info(f"🚀 [AI 서버 전송] Request ID: {request_id}")

                try:
                    result = await send_request_to_ai_server(request_data)
                    logger.info(f"✅ [완료] Request ID: {request_id} | Result: {result}")
                except Exception as e:
                    logger.error(f"❌ [실패] Request ID: {request_id} | Error: {e}")
                finally:
                    self.request_queue.task_done()
        finally:
            self.is_worker_running = False
            self.AI_server_status = False

    def set_ai_status(self, status: bool):
        """AI 서버 상태를 설정"""
        self.AI_server_status = status
        logger.info(f"🔄 AI 서버 상태: {'READY' if status else 'DOWN'}")

# 싱글톤 패턴으로 QueueService 인스턴스 생성
queue_service = QueueService()
