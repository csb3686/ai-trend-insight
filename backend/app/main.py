from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from app.core.config import get_settings
from app.core.database import get_db
from app.schemas.chat import HealthCheck

settings = get_settings()

app = FastAPI(
    title="TrendRadar API",
    description="AI 기술 트렌드 인사이트 플랫폼 API 서버",
    version="1.0.0"
)

# CORS 설정 (프론트엔드 연동 대비)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 단계에서는 모두 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "TrendRadar API Server is running."}

@app.get("/api/v1/health", response_model=HealthCheck, tags=["System"])
async def health_check(db: Session = Depends(get_db)):
    """
    서버 및 데이터베이스 연결 상태를 확인합니다.
    """
    try:
        # DB 연결 테스트 (SQLAlchemy 2.0에서는 text() 필수)
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "ok",
        "database": db_status,
        "timestamp": datetime.now()
    }

# 향후 라우터 등록 예시
# from app.api.endpoints import chat, trends
# app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
