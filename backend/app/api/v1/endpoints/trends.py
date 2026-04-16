from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.trend_service import trend_service
from app.schemas.trend import (
    TrendHeatmapResponse, 
    TrendTop5Response, 
    TrendTimelineResponse,
    KeywordItem,
    DashboardSummaryResponse
)

router = APIRouter()

@router.get("/summary", response_model=DashboardSummaryResponse)
async def get_summary(db: Session = Depends(get_db)):
    """대시보드 상단 통계 요약 정보를 조회합니다."""
    return trend_service.get_dashboard_summary(db)

@router.get("/heatmap", response_model=TrendHeatmapResponse)
async def get_heatmap(
    year: Optional[int] = Query(None, description="연도 (기본값: 최신 데이터)"),
    month: Optional[int] = Query(None, description="월 (기본값: 최신 데이터)"),
    db: Session = Depends(get_db)
):
    """기술별 언급 빈도 데이터를 조회하여 히트맵 형식으로 제공합니다."""
    y, m, data = trend_service.get_heatmap_data(db, year, month)
    return TrendHeatmapResponse(year=y, month=m, data=data)

@router.get("/top5", response_model=TrendTop5Response)
async def get_top5(
    year: Optional[int] = Query(None, description="연도 (기본값: 최신 데이터)"),
    month: Optional[int] = Query(None, description="월 (기본값: 최신 데이터)"),
    db: Session = Depends(get_db)
):
    """전월 대비 언급량 변화율 기준 상·하위 5개 기술을 조회합니다."""
    return trend_service.get_top5_trends(db, year, month)

@router.get("/timeline/{tech_id}", response_model=TrendTimelineResponse)
async def get_timeline(
    tech_id: int,
    db: Session = Depends(get_db)
):
    """특정 기술의 연도/월별 언급량 추이 및 인사이트 분석 결과를 조회합니다."""
    result = trend_service.get_tech_timeline(db, tech_id)
    if not result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Technology not found")
        
    return result

@router.get("/keywords", response_model=List[KeywordItem])
async def get_keywords(db: Session = Depends(get_db)):
    """현재 시스템에 등록된 모든 활성 기술 키워드 목록을 조회합니다."""
    results = trend_service.get_all_keywords(db)
    return [KeywordItem(id=r.id, name=r.name, category=r.category) for r in results]
