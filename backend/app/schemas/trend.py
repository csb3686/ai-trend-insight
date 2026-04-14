from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class TrendHeatmapItem(BaseModel):
    """히트맵용 기술 트렌드 항목"""
    tech_id: int
    name: str = Field(..., description="기술명")
    category: str = Field(..., description="기술 카테고리")
    mention_count: int = Field(..., description="언급 횟수")
    rank: int = Field(..., description="현재 순위")
    change_rate: Optional[Decimal] = Field(None, description="전월 대비 변화율")

class TrendHeatmapResponse(BaseModel):
    """히트맵 응답 스키마"""
    year: int
    month: int
    data: List[TrendHeatmapItem]

class TrendTopItem(BaseModel):
    """순위권 기술 항목 (상승/하락)"""
    name: str
    category: str
    change_rate: Decimal
    rank: int

class TrendTop5Response(BaseModel):
    """상승/하락 Top 5 응답"""
    rising: List[TrendTopItem]
    falling: List[TrendTopItem]

class TrendTimelineItem(BaseModel):
    """시계열 데이터 항목"""
    year: int
    month: int
    mention_count: int
    rank: int

class TrendTimelineResponse(BaseModel):
    """특정 기술의 시계열 응답"""
    tech_id: int
    name: str
    timeline: List[TrendTimelineItem]

class KeywordItem(BaseModel):
    """기술 키워드 정보"""
    id: int
    name: str
    category: str

class DashboardSummaryResponse(BaseModel):
    """대시보드 상단 통계 요약 응답"""
    news_count: int
    github_count: int
    tech_count: int
    last_updated: str
    updated_minutes_ago: int
