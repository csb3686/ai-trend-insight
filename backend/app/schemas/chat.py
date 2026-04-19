from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    """채팅 요청 스키마"""
    message: str

class SourceItem(BaseModel):
    """참고 소식 아이템 스키마"""
    title: str
    url: str

class ChatResponse(BaseModel):
    """채팅 응답 스키마"""
    answer: str
    context: Optional[str] = None
    sources: List[SourceItem] = []

class HealthCheck(BaseModel):
    """서버 상태 체크 스키마"""
    status: str
    database: str
    timestamp: datetime
    gemini_models: Optional[List[str]] = []
