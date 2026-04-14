from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class SourceInfo(BaseModel):
    """출처 정보"""
    id: int
    name: str
    url: str

class ArticleListItem(BaseModel):
    """목록용 기사 요약 정보"""
    id: int
    title: str
    url: str
    source_name: str
    type: str
    tech_category: Optional[str] = "Others" # 추가: 범례 배지용 카테고리
    published_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class ArticleDetail(BaseModel):
    """기사 상세 정보"""
    id: int
    title: str
    url: str
    content: Optional[str]
    description: Optional[str]
    author: Optional[str]
    type: str
    source: SourceInfo
    published_at: Optional[datetime]
    
    # GitHub 전용
    github_stars: Optional[int] = None
    github_language: Optional[str] = None
    
    # 연관 기술
    technologies: List[str] = []

    class Config:
        from_attributes = True

class ArticleListResponse(BaseModel):
    """기사 목록 응답"""
    total: int
    items: List[ArticleListItem]
