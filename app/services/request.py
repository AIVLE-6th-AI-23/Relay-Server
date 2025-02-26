import httpx
import logging
import asyncio
from app.constants import AI_SERVER_URL, HEADERS

logger = logging.getLogger(__name__)

async def send_request_to_ai_server(request_data):
    """AI 서버에 요청을 보내는 함수 (지수 백오프 포함)"""
    url = f"{AI_SERVER_URL}/analyze/start"
    for attempt in range(1, 4):  # 최대 3회 재시도
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=request_data, headers=HEADERS)
                if response.status_code == 200:
                    logger.info(f"✅ AI 서버 요청 성공: {response.json()}")
                    return response.json()
                else:
                    logger.warning(f"⚠️ AI 서버 응답 실패: {response.status_code}")
        except Exception as e:
            logger.error(f"🚨 AI 서버 요청 실패 (시도 {attempt}): {e}")
        await asyncio.sleep(2 ** attempt)  # 지수 백오프 (2, 4, 8초)
    raise Exception("AI 서버 요청 실패 (재시도 초과)")
