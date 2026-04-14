from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.admin_service import admin_service
from app.schemas.admin import HealthCheckDetail, CollectionLogResponse, TaskTriggerResponse

router = APIRouter()

@router.get("/health/detail", response_model=HealthCheckDetail, tags=["Health"])
async def get_health_detail(db: Session = Depends(get_db)):
    """
    시스템 주요 컴포넌트(MySQL, Chroma, LLM)의 상태를 상세 진단합니다.
    """
    return await admin_service.check_system_health(db)

@router.get("/admin/collection-logs", response_model=List[CollectionLogResponse], tags=["Admin"])
def get_collection_logs(limit: int = 20, db: Session = Depends(get_db)):
    """
    최근 수집 및 임베딩 처리 이력 로그를 조회합니다.
    """
    return admin_service.get_collection_logs(db, limit)

@router.post("/admin/collect", response_model=TaskTriggerResponse, tags=["Admin"])
async def trigger_collect(background_tasks: BackgroundTasks):
    """
    데이터 수집 작업을 수동으로 트리거합니다 (백그라운드 실행).
    """
    # 주의: 실제 운영 환경에서는 SessionLocal 팩토리를 넘겨줘야 함
    from app.core.database import SessionLocal
    background_tasks.add_task(admin_service.run_collection_task, SessionLocal, "COLLECT")
    return TaskTriggerResponse(message="데이터 수집 작업이 백그라운드에서 시작되었습니다.")

@router.post("/admin/embed", response_model=TaskTriggerResponse, tags=["Admin"])
async def trigger_embed(background_tasks: BackgroundTasks):
    """
    미처리 기사들에 대한 벡터 임베딩 작업을 수동으로 트리거합니다 (백그라운드 실행).
    """
    from app.core.database import SessionLocal
    background_tasks.add_task(admin_service.run_collection_task, SessionLocal, "EMBED")
    return TaskTriggerResponse(message="벡터 임베딩 작업이 백그라운드에서 시작되었습니다.")

@router.post("/admin/recompute-stats", response_model=TaskTriggerResponse, tags=["Admin"])
async def trigger_recompute_stats(background_tasks: BackgroundTasks):
    """
    전체 기술 트렌드 통계 재계산 작업을 수동으로 트리거합니다.
    """
    from app.core.database import SessionLocal
    background_tasks.add_task(admin_service.run_collection_task, SessionLocal, "STATS")
    return TaskTriggerResponse(message="트렌드 통계 재계산 작업이 시작되었습니다.")
