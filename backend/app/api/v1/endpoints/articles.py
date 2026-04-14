from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.article_service import article_service
from app.schemas.article import ArticleListItem, ArticleDetail, ArticleListResponse

router = APIRouter()

@router.get("/", response_model=ArticleListResponse)
async def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    type: Optional[str] = Query(None, description="기사 유형 (news, github_repo)"),
    source_id: Optional[int] = Query(None, description="출처 ID 필터"),
    db: Session = Depends(get_db)
):
    """뉴스 기사 및 GitHub 트렌딩 목록을 조회합니다."""
    total, items = article_service.get_articles(db, skip, limit, type, source_id)
    return ArticleListResponse(total=total, items=items)

@router.get("/tech/{tech_id}", response_model=List[ArticleListItem])
async def get_articles_by_tech(
    tech_id: int,
    limit: int = Query(3, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """특정 기술이 언급된 최신 뉴스 목록을 조회합니다. (히트맵 상세 패널용)"""
    return article_service.get_articles_by_tech(db, tech_id, limit)

@router.get("/{article_id}", response_model=ArticleDetail)
async def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """특정 기사의 상세 정보 및 연관 기술 목록을 조회합니다."""
    article = article_service.get_article_by_id(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
