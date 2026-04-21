from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Any
from app.core.database import get_db
from app.services.analysis_service import analysis_service

router = APIRouter()

@router.get("/tech-ecosystem", tags=["Analysis"])
def get_tech_ecosystem(db: Session = Depends(get_db)) -> Any:
    """
    기술 간의 상관관계를 분석한 네트워크 그래프 데이터를 반환합니다.
    Cytoscape.js에서 즉시 사용할 수 있는 형식입니다.
    """
    return analysis_service.get_tech_ecosystem(db, limit=30)
