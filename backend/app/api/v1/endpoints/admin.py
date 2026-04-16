from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.config import get_settings
from app.services.admin_service import admin_service
from app.schemas.admin import HealthCheckDetail, CollectionLogResponse, TaskTriggerResponse

settings = get_settings()
router = APIRouter()

def verify_admin_token(x_admin_token: str = Header(...)):
    """ADMIN_TOKEN 일치 여부를 검증하는 의존성 함수"""
    if x_admin_token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Invalid Admin Token")
    return x_admin_token

@router.get("/health/detail", response_model=HealthCheckDetail, tags=["Health"])
async def get_health_detail(db: Session = Depends(get_db)):
    """시스템 주요 컴포넌트(MySQL, Chroma, LLM)의 상태를 상세 진단합니다."""
    return await admin_service.check_system_health(db)

@router.get("/admin/collection-logs", response_model=List[CollectionLogResponse], tags=["Admin"], dependencies=[Depends(verify_admin_token)])
def get_collection_logs(limit: int = 20, db: Session = Depends(get_db)):
    """최근 수집 및 임베딩 처리 이력 로그를 조회합니다."""
    return admin_service.get_collection_logs(db, limit)

# --- 신기술 승인 관리 API ---

@router.get("/admin/pending-tech")
def get_pending(db: Session = Depends(get_db)):
    print("--- [DEBUG] GET /admin/pending-tech 진입 ---")
    return admin_service.get_pending_technologies(db)

@router.get("/admin/stats")
def get_stats(db: Session = Depends(get_db)):
    print("--- [DEBUG] GET /admin/stats 진입 ---")
    return admin_service.get_embedding_stats(db)

@router.get("/admin/collection-logs")
def get_logs(db: Session = Depends(get_db)):
    print("--- [DEBUG] GET /admin/collection-logs 진입 ---")
    return admin_service.get_collection_logs(db)

@router.post("/admin/approve-tech/{id}", tags=["Admin"], dependencies=[Depends(verify_admin_token)])
def approve_pending_tech(id: int, db: Session = Depends(get_db)):
    """신규 기술을 최종 승인하여 정식 등록합니다."""
    success = admin_service.approve_technology(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Pending tech not found")
    return {"status": "success", "message": "Technology approved and registered"}

@router.post("/admin/reject-tech/{id}", tags=["Admin"], dependencies=[Depends(verify_admin_token)])
def reject_pending_tech(id: int, db: Session = Depends(get_db)):
    """신규 기술 후보를 거절하여 삭제합니다."""
    success = admin_service.reject_technology(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Pending tech not found")
    return {"status": "success", "message": "Technology candidate rejected"}

# --- 수동 작업 실행 API ---

@router.post("/admin/collect", response_model=TaskTriggerResponse, tags=["Admin"], dependencies=[Depends(verify_admin_token)])
async def trigger_collect(background_tasks: BackgroundTasks):
    """
    데이터 수집 작업을 수동으로 트리거합니다 (백그라운드 실행).
    """
    from app.core.database import SessionLocal
    background_tasks.add_task(admin_service.run_collection_task, SessionLocal, "COLLECT")
    return TaskTriggerResponse(message="데이터 수집 작업이 백그라운드에서 시작되었습니다.")

@router.post("/admin/embed", response_model=TaskTriggerResponse, tags=["Admin"], dependencies=[Depends(verify_admin_token)])
async def trigger_embed(background_tasks: BackgroundTasks):
    """
    미처리 기사들에 대한 벡터 임베딩 작업을 수동으로 트리거합니다 (백그라운드 실행).
    """
    from app.core.database import SessionLocal
    background_tasks.add_task(admin_service.run_collection_task, SessionLocal, "EMBED")
    return TaskTriggerResponse(message="벡터 임베딩 작업이 백그라운드에서 시작되었습니다.")

@router.post("/admin/recompute-stats", response_model=TaskTriggerResponse, tags=["Admin"], dependencies=[Depends(verify_admin_token)])
async def trigger_recompute_stats(background_tasks: BackgroundTasks):
    """
    전체 기술 트렌드 통계 재계산 작업을 수동으로 트리거합니다.
    """
    from app.core.database import SessionLocal
    background_tasks.add_task(admin_service.run_collection_task, SessionLocal, "STATS")
    return TaskTriggerResponse(message="트렌드 통계 재계산 작업이 시작되었습니다.")

@router.get("/admin/stats", tags=["Admin"], dependencies=[Depends(verify_admin_token)])
def get_admin_stats(db: Session = Depends(get_db)):
    """시스템 임베딩 및 데이터 통계를 조회합니다."""
    return admin_service.get_embedding_stats(db)

@router.post("/admin/reset-db", tags=["Admin"], dependencies=[Depends(verify_admin_token)])
def reset_vector_db_state(db: Session = Depends(get_db)):
    """벡터 DB 상태를 리셋하여 전체 재학습이 가능하도록 합니다."""
    return admin_service.reset_vector_db(db)
