from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class HealthStatus(str, Enum):
    OK = "ok"
    ERROR = "error"
    WARNING = "warning"

class ComponentHealth(BaseModel):
    status: HealthStatus
    message: Optional[str] = None
    latency_ms: Optional[float] = None

class HealthCheckDetail(BaseModel):
    """시스템 정밀 진단 결과 스키마"""
    status: HealthStatus
    timestamp: datetime = Field(default_factory=datetime.now)
    components: Dict[str, ComponentHealth]

class CollectionLogResponse(BaseModel):
    """수집 로그 응답 스키마"""
    id: int
    task_type: str
    start_time: datetime
    end_time: Optional[datetime]
    status: str
    collected_count: int
    processed_count: int
    error_message: Optional[str]
    triggered_by: str

    class Config:
        from_attributes = True

class TaskTriggerResponse(BaseModel):
    """수동 작업 트리거 응답"""
    message: str
    task_id: Optional[int] = None
    status: str = "accepted"
