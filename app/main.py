import logging
from fastapi import FastAPI
from app.routes import analyze, status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 인스턴스 생성
app = FastAPI(title="Relay Server with AI Queue")

# 라우트 등록
app.include_router(analyze.router, tags=["Analyze"])
app.include_router(status.router, tags=["Status"])

logger.info("🚀 Relay Server is running...")
